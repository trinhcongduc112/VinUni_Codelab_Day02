"""Offline checks of rejection paths; these are not live model evaluations."""
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
import pytest

spec = importlib.util.spec_from_file_location('prototype', Path(__file__).resolve().parents[1] / 'starter-code/prompt_prototype.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


def payload(**changes):
    data = dict(action='request_human_review', reason='Thiếu dữ liệu', draft='[DRAFT_ONLY] Cần người kiểm tra', station_name='', requires_approval=True, sent=False)
    data.update(changes)
    return json.dumps(data)


@pytest.mark.parametrize('changes', [dict(sent=True), dict(requires_approval=False), dict(requires_approval=1), dict(draft='Đã gửi'), dict(draft='[DRAFT_ONLY] Chúng tôi đang điều động xe'), dict(action='send_now'), dict(station_name='Trạm bịa'), dict(action='recommend_station'), dict(reason='')])
def test_reject_unsafe_fields(changes):
    with pytest.raises(ValueError):
        p.validate_response(payload(**changes))


@pytest.mark.parametrize('raw', ['', 'not json', '[]', '{}', '{"sent":false'])
def test_reject_malformed_output(raw):
    with pytest.raises(ValueError):
        p.validate_response(raw)


def test_timeout_is_a_failure_not_a_pass(monkeypatch):
    def timeout(_):
        raise TimeoutError()
    monkeypatch.setattr(p, 'evaluate_prompt', timeout)
    assert p.run_case(p.ADVERSARIAL_TESTS[0])['status'] == 'Failed'


def test_wrong_action_is_rejected(monkeypatch):
    monkeypatch.setattr(p, 'evaluate_prompt', lambda _: p.TAG + '\n' + payload())
    assert p.run_case(p.ADVERSARIAL_TESTS[0])['status'] == 'Failed'


def test_missing_key_does_not_call_api(monkeypatch):
    monkeypatch.delenv('GEMINI_API_KEY', raising=False)
    monkeypatch.delenv('GOOGLE_API_KEY', raising=False)
    with pytest.raises(RuntimeError, match='Missing'):
        p.evaluate_prompt('test')


def test_sdk_receives_system_instruction_and_schema(monkeypatch):
    from google import genai
    observed = {}
    class Client:
        def __init__(self, **kwargs):
            self.models = self
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def generate_content(self, **kwargs):
            observed.update(kwargs)
            return SimpleNamespace(text=payload())
    monkeypatch.setenv('GEMINI_API_KEY', 'fake-test-key')
    monkeypatch.setattr(genai, 'Client', Client)
    assert p.evaluate_prompt('untrusted').startswith(p.TAG + '\n')
    assert observed['contents'] == 'untrusted'
    assert observed['config'].system_instruction == p.SYSTEM_PROMPT
    assert observed['config'].response_mime_type == 'application/json'

@pytest.mark.parametrize('bad_action,expected_exit', [(False, 0), (True, 1)])
def test_batch_runner_checks_each_result_and_saves_report(monkeypatch, tmp_path, bad_action, expected_exit):
    cases = p.ADVERSARIAL_TESTS + p.CONTROL_TESTS
    def fake_evaluate(text, batch_size=0):
        assert batch_size == len(cases)
        assert json.loads(text) == [case['input'] for case in cases]
        results = [json.loads(payload(action=case['expected_action'], station_name=case.get('expected_station', ''))) for case in cases]
        if bad_action:
            results[0]['action'] = 'request_human_review'
        return p.TAG + '\n' + json.dumps(results)
    report = tmp_path / 'results.json'
    monkeypatch.setenv('GEMINI_API_KEY', 'fake-test-key')
    monkeypatch.setattr(p, 'evaluate_prompt', fake_evaluate)
    monkeypatch.setattr(p.sys, 'argv', ['prototype', '--report', str(report)])
    assert p.main() == expected_exit
    data = json.loads(report.read_text(encoding='utf-8'))
    assert data['mode'] == 'live_gemini_batch'
    assert len(data['results']) == len(cases)
    assert data['results'][0]['status'] == ('Failed' if bad_action else 'Passed')

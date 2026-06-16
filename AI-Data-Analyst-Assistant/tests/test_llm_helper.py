"""
Unit tests for utils/llm_helper.py
"""
import pytest
import os
import json
from unittest.mock import patch

from utils.llm_helper import LLMHelper


@pytest.fixture
def helper():
    """LLMHelper with no API key set."""
    with patch.dict(os.environ, {}, clear=True):
        return LLMHelper()


@pytest.fixture
def helper_with_key():
    """LLMHelper with a dummy API key."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key-123"}):
        return LLMHelper()


@pytest.fixture
def sample_analysis():
    return {
        "shape": (100, 5),
        "columns": ["id", "name", "sales", "region", "date"],
        "missing_values": {"id": 0, "name": 2, "sales": 1, "region": 0, "date": 3},
        "statistics": {"sales": {"mean": 500, "std": 100}},
        "duplicate_rows": 5
    }


class TestLLMHelperInit:
    def test_init_no_api_key(self, helper):
        assert helper.api_key is None

    def test_init_with_api_key(self, helper_with_key):
        assert helper_with_key.api_key == "test-key-123"

    def test_default_model(self, helper):
        assert helper.model == "gpt-3.5-turbo"

    def test_custom_model(self):
        with patch.dict(os.environ, {"LLM_MODEL": "gpt-4", "OPENAI_API_KEY": ""}):
            h = LLMHelper()
            assert h.model == "gpt-4"


class TestFormatPrompt:
    def test_format_prompt_contains_shape(self, helper, sample_analysis):
        prompt = helper._format_prompt(sample_analysis)
        assert "(100, 5)" in prompt

    def test_format_prompt_contains_columns(self, helper, sample_analysis):
        prompt = helper._format_prompt(sample_analysis)
        assert "sales" in prompt
        assert "region" in prompt

    def test_format_prompt_contains_missing_values(self, helper, sample_analysis):
        prompt = helper._format_prompt(sample_analysis)
        assert "missing_values" in prompt.lower() or "Missing Values" in prompt

    def test_format_prompt_contains_duplicate_rows(self, helper, sample_analysis):
        prompt = helper._format_prompt(sample_analysis)
        assert "5" in prompt

    def test_format_prompt_is_stripped(self, helper, sample_analysis):
        prompt = helper._format_prompt(sample_analysis)
        assert not prompt.startswith("\n")
        assert not prompt.endswith("\n")


class TestCallLLM:
    def test_no_api_key_returns_message(self, helper):
        result = helper._call_llm("test prompt")
        assert "API key not configured" in result

    def test_with_api_key_returns_placeholder(self, helper_with_key):
        result = helper_with_key._call_llm("test prompt")
        assert "not yet implemented" in result


class TestGetInsights:
    def test_get_insights_no_key(self, helper, sample_analysis):
        result = helper.get_insights(sample_analysis)
        assert "API key not configured" in result

    def test_get_insights_with_key(self, helper_with_key, sample_analysis):
        result = helper_with_key.get_insights(sample_analysis)
        assert "not yet implemented" in result

    def test_get_insights_handles_empty_analysis(self, helper):
        result = helper.get_insights({})
        assert isinstance(result, str)


class TestGenerateReport:
    def test_report_contains_header(self, helper, sample_analysis):
        report = helper.generate_report(sample_analysis)
        assert "Data Analysis Report" in report

    def test_report_contains_shape(self, helper, sample_analysis):
        report = helper.generate_report(sample_analysis)
        assert "(100, 5)" in report

    def test_report_contains_columns(self, helper, sample_analysis):
        report = helper.generate_report(sample_analysis)
        assert "sales" in report
        assert "region" in report

    def test_report_contains_data_quality(self, helper, sample_analysis):
        report = helper.generate_report(sample_analysis)
        assert "Missing Values" in report
        assert "Duplicate Rows" in report

    def test_report_is_stripped(self, helper, sample_analysis):
        report = helper.generate_report(sample_analysis)
        assert not report.startswith("\n")

    def test_report_with_empty_analysis(self, helper):
        report = helper.generate_report({})
        assert "Data Analysis Report" in report

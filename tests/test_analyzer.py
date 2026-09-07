from datetime import datetime, timezone, timedelta
from src.analyzer import RepoAnalyzer


def test_score_to_grade():
    analyzer = RepoAnalyzer()
    assert analyzer._score_to_grade(95.0) == "A+"
    assert analyzer._score_to_grade(85.0) == "A"
    assert analyzer._score_to_grade(75.0) == "B"
    assert analyzer._score_to_grade(65.0) == "C"
    assert analyzer._score_to_grade(55.0) == "D"
    assert analyzer._score_to_grade(40.0) == "F"


def test_calculate_maintenance_score():
    analyzer = RepoAnalyzer()
    now = datetime.now(timezone.utc)

    # Recent update (within 30 days) -> Max score
    recent_date = now - timedelta(days=10)
    assert analyzer._calculate_maintenance_score(recent_date) == 1.0

    # Stale update (> 1 year) -> Low score
    old_date = now - timedelta(days=400)
    assert analyzer._calculate_maintenance_score(old_date) == 0.1


def test_analyze_portfolio_empty():
    analyzer = RepoAnalyzer()
    result = analyzer.analyze_portfolio([])
    assert result["total_repos"] == 0
    assert result["overall_score"] == 0.0
    assert result["grade"] == "N/A"
    assert len(result["recommendations"]) == 1
from automation import lab


def test_complete_demo(tmp_path, monkeypatch):
    monkeypatch.setattr(lab,"GENERATED",tmp_path/"generated")
    monkeypatch.setattr(lab,"DB",tmp_path/"generated"/"entra.sqlite3")
    monkeypatch.setattr(lab,"REPORTS",tmp_path/"generated"/"reports")
    assert lab.run_demo() == 0
    assert lab.validate() == 0
    assert (lab.REPORTS/"investigation.json").exists()


def test_failure_has_nonzero_normal_validation(tmp_path, monkeypatch):
    monkeypatch.setattr(lab,"GENERATED",tmp_path/"generated")
    monkeypatch.setattr(lab,"DB",tmp_path/"generated"/"entra.sqlite3")
    monkeypatch.setattr(lab,"REPORTS",tmp_path/"generated"/"reports")
    lab.setup(); lab.introduce_failure()
    assert lab.validate() == 2
    assert lab.validate(expect_failure=True) == 0


def test_setup_is_idempotent(tmp_path, monkeypatch):
    monkeypatch.setattr(lab,"GENERATED",tmp_path/"generated")
    monkeypatch.setattr(lab,"DB",tmp_path/"generated"/"entra.sqlite3")
    monkeypatch.setattr(lab,"REPORTS",tmp_path/"generated"/"reports")
    assert lab.setup() == lab.setup() == 0
    with lab.connect() as con:
        assert con.execute("SELECT count(*) FROM identities").fetchone()[0] == 2

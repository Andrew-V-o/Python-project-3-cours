from lab.main import main


def test_cli_exit(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "0")
    
    try:
        main()
    except SystemExit as e:
        assert e.code == 0
        
    captured = capsys.readouterr()
    assert "Завершение работы программы." in captured.out
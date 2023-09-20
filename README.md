# FastAPIでBasic認証検証レポジトリ

## Setup(asdf前提)

asdfというパッケージマネージャーを使うので、それをインストールしてから。Homebrewで入るはず。

VSCodeで本プロジェクトを開いたら、ターミナルより以下のコマンドを順番に打てばOK

- `asdf plugin-add python`
- `asdf plugin-add poetry`
- `asdf install`
- `poetry config virtualenvs.in-project true`
- `poetry install`
- `poetry shell`
- `uvicorn main:app --reload`
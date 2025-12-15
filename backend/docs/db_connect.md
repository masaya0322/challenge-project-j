# Database Connection Documentation

## 概要

`db_connect.py` は、SQLAlchemy を使用してデータベース接続を確立し、セッション管理を行うためのモジュールです。

SQLAlchemy とは
SQLAlchemy とは，Python の中でよく利用されている ORM の 1 つ．
ORM とは，Object Relational Mapper のことで，簡単に説明すると，テーブルとクラスを 1 対 1 に対応させて，そのクラスのメソッド経由でデータを取得したり，変更したりできるようにする存在．
https://qiita.com/arkuchy/items/75799665acd09520bed2

アプリケーション全体で使用されるデータベースセッションとベースモデルを提供します。

### 使用方法

```python
from db_connect import SessionLocal, Base, engine

# テーブル作成
Base.metadata.create_all(bind=engine)

# セッション利用
db = SessionLocal()
try:
    # データベース操作
    pass
finally:
    db.close()
```

## 設定項目

- `DATABASE_URL`: データベース接続文字列。環境変数から取得します。
  - デフォルト値: `postgresql://user:password@localhost:5432/mydb`

## 処理フロー

1. `create_engine` を使用して、`DATABASE_URL` に基づくデータベースエンジンを作成します。
2. `sessionmaker` を使用して、`SessionLocal` クラス（セッションファクトリ）を作成します。
   - `autocommit=False`, `autoflush=False` に設定されています。
3. `declarative_base` を使用して、ORM モデルの基底クラス `Base` を作成します。
4. `get_db` 関数が呼び出されると、`SessionLocal` から新しいセッションインスタンスを生成し、呼び出し元に提供（yield）します。
5. 処理が完了すると、`finally` ブロックでセッションを閉じます。

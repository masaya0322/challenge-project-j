ブランチ名：(feature,add,fix,refactor)/#ISSUE番号/ISSUEタイトル
英語で統一すること

導入
# Dockerがインストールされていることを確認
docker --version
# カレントディレクトリ移動
cd backend
# コンテナをビルド
docker build -t cpj-backend-app .
# 実行
docker run -d -p 8000:8000 --name cpj-backend cpj-backend-app

# テスト
http://localhost:8000/api/hello
にアクセスすると、Hello Worldが返される
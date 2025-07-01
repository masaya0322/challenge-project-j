

前提
cdはchallenge-project-jである

# backend導入
## Dockerがインストールされていることを確認
docker --version
## カレントディレクトリ移動
cd backend
## コンテナをビルド
docker build -t cpj-backend-app .
## 実行
docker run -d -p 8000:8000 --name cpj-backend cpj-backend-app
## テスト
curl http://localhost:8000/api/hello

# テスト
http://localhost:8000/api/hello
にアクセスすると、Hello Worldが返される
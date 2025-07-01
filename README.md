# お片付けレンジャー - Okatazuke Ranger

おもちゃ箱 × ゲーム × IoT。  
Raspberry Pi と RFID リーダーを使って、片付けをゲーム化するプロジェクトです。

## 技術構成 / Tech Stack

- Frontend: [Next.js (TypeScript)](https://nextjs.org/)
- Backend: [FastAPI (Python)](https://fastapi.tiangolo.com/)
- Container: Docker / Docker Compose
- Package Manager: [pnpm](https://pnpm.io/)

## 起動方法 / How to Run

### 1. このリポジトリをクローン

```bash
git clone https://github.com/masaya0322/challenge-project-j.git
```

### 2.このリモートリポジトリに変更を反映させる方法

```bash
git add.
git commit -m "コミットメッセージ"
git push
```

### 3.このリモートリポジトリの変更をローカルに反映させる方法

``` bash
mainブランチの場合：git pull
他ブランチの場合は相談すること
```

## backend
前提
cdはchallenge-project-jである

### 1.Dockerがインストールされていることを確認
docker --version
### 2.カレントディレクトリ移動
cd backend
### 3.コンテナをビルド
docker build -t cpj-backend-app .
### 4.実行
docker run -d -p 8000:8000 --name cpj-backend cpj-backend-app
### 5.テスト
curl http://localhost:8000/api/hello

### テスト
http://localhost:8000/api/hello
にアクセスすると、Hello Worldが返される
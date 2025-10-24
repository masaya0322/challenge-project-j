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

## backendの起動方法
前提
- パスはchallenge-project-jであること
- Docker Desktopが起動していること

### 1. dockerとdocker-composeがインストールされているかを確認

``` bash
docker --version
docker-compose --version
```

### 2. カレントディレクトリを移動

``` bash
cd backend
```
### 3. コンテナを作成
初めてコンテナを作成する場合は、docker-composeを用いてbuildをする必要がある。3.1.に進む

すでにコンテナを作成済みの場合は、docker-composeを用いて、コンテナを起動するだけで良い。3.2.に進む

3.2.の方法だと、ターミナルが1つ占有される。バックグラウンドで起動したい場合は3.3.に進む

### 3.1. 初めてコンテナを作成、起動する場合

``` bash
docker-compose up --build
```

### 3.2. コンテナを作成済みで起動する場合
既存のコンテナを起動するだけなので、buildは不要。
``` bash
docker-compose up
```

### 3.3. バックエンドで起動する場合
`docker-compose up`に`-d`オプションを追加する。
コンテナ作成済みの場合
``` bash
docker-compose up -d
```

### 4. 動作確認
別のターミナルを開き、

``` bash
curl http://localhost:8000/api/hello
```
を実行して、`Hello World`が帰ってくれば成功。

### コピー用
初めてコンテナを作成、起動する場合
``` bash
docker --version
docker-compose --version
cd backend
docker-compose up --build
```

コンテナを作成済みで起動する場合
``` bash
cd backend
docker-compose up
```

### コンテナを停止する
フォアグラウンドで起動している場合は、`CTRL + C`で停止。
バックグラウンドで起動している場合は、`docker-compose down`で停止。

### 備考
- コード変更時に再ビルドする必要はない。（`docker-compose.yml`上で、`--reload`オプションを有効にしているため）
- requirements.txtを変更した場合は、`docker-compose up --build`を再び行う必要がある
- コンテナを削除して、もう一度ビルドし直したい場合は、`docker-compose down --rmi all`を実行して、`docker-composte up --build`を実行する
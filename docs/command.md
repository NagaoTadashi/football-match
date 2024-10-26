## FastAPI 開発サーバーの起動

vicorn app.main:app --reload

## nuxt.js 開発サーバーの起動

npm run dev -- -o

## データベース操作関係

# マイグレーションファイルの生成

alembic revision --autogenerate -m "コメント"

# マイグレーションの適用

alembic upgrade head

# Artifact Registory

# コンテナのビルド

docker build -t us-central1-docker.pkg.dev/football-match-439708/football-match-nuxt/nuxt-app:latest -f Dockerfile.production .

docker build -t us-central1-docker.pkg.dev/football-match-439708/football-match-fastapi/fastapi-app:latest -f Dockerfile.production .

#　 push

docker push us-central1-docker.pkg.dev/football-match-439708/football-match-nuxt/nuxt-app:latest

docker push us-central1-docker.pkg.dev/football-match-439708/football-match-fastapi/fastapi-app:latest

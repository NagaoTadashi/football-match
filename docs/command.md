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

docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/web-league-441014/nuxt/nuxt:latest -f Dockerfile.production .

docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/web-league-441014/fastapi/fastapi:latest -f Dockerfile.production .

# push

docker push us-central1-docker.pkg.dev/web-league-441014/nuxt/nuxt:latest

docker push us-central1-docker.pkg.dev/web-league-441014/fastapi/fastapi:latest

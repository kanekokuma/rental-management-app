# 学内備品貸出管理システム

Djangoで作成した、PC・VRゴーグルなどの貸出管理システムです。
学生は備品一覧の確認と貸出申請、管理者は備品管理・返却処理・履歴確認を行えます。

## 主な機能

- ログイン / ログアウト
- 備品一覧表示
- 備品詳細表示
- 貸出申請
- 貸出中一覧
- 返却処理
- 貸出履歴
- 管理者による備品追加・編集・削除
- 返却期限超過の表示
- 種類・状態による絞り込み
- Render / PostgreSQL でのクラウド公開

## ローカル実行手順

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_items
python manage.py createsuperuser
python manage.py runserver
```

ブラウザで以下にアクセスします。

```text
http://127.0.0.1:8000/
```

## 管理者画面

```text
http://127.0.0.1:8000/admin/
```

## 学生ユーザーと管理者ユーザー

- 学生ユーザー: `is_staff` をオフ
- 管理者ユーザー: `is_staff` をオン

## 環境変数

`.env.example` を参考に、クラウド側で以下を設定します。

```text
SECRET_KEY=本番用のランダムな値
DEBUG=False
ALLOWED_HOSTS=公開ホスト名
CSRF_TRUSTED_ORIGINS=https://公開ホスト名
DATABASE_URL=PostgreSQLの接続URL
```

Render の場合は `render.yaml` を使うと、WebサービスとPostgreSQLをまとめて作成できます。

## Render公開手順

1. このディレクトリをGitHubリポジトリにpushします。
2. Renderで「New +」から「Blueprint」を選び、リポジトリを接続します。
3. `render.yaml` の設定でWebサービスとPostgreSQLを作成します。
4. 初回デプロイ後、RenderのShellで管理者を作成します。

```bash
python manage.py createsuperuser
```

## Renderを手動設定する場合

Build Command:

```bash
bash build.sh
```

Start Command:

```bash
gunicorn equipment_rental.wsgi:application
```

## テスト

```bash
python manage.py test
```

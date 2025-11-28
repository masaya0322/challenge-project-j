# Frontend Development Guide

このドキュメントは、本プロジェクトのフロントエンド開発におけるガイドラインと規約をまとめたものです。

## 技術スタック

- **Next.js 16**: React フレームワーク
- **React 19**: UI ライブラリ
- **Tailwind CSS 4**: ユーティリティファーストの CSS フレームワーク
- **shadcn/ui**: 再利用可能な UI コンポーネント
- **TypeScript**: 型安全な開発

## セットアップ

```bash
# 依存関係のインストール
npm install

# 開発サーバーの起動
npm run dev

# ビルド
npm run build

# 本番サーバーの起動
npm run start
```

## コーディング規約

### ファイル命名規則

- **ケバブケース（kebab-case）を使用する**
  ```
  ✅ user-profile.tsx
  ✅ api-client.ts
  ✅ use-user-data.ts
  ❌ UserProfile.tsx
  ❌ apiClient.ts
  ❌ useUserData.ts
  ```

### Export 規則

- **default export はページコンポーネント以外で使用しない**
  ```typescript
  // ✅ ページコンポーネント (app/page.tsx, app/about/page.tsx など)
  export default function HomePage() {
    return <div>...</div>
  }

  // ✅ 通常のコンポーネント
  export function UserProfile() {
    return <div>...</div>
  }

  // ❌ 通常のコンポーネントで default export を使用
  export default function UserProfile() {
    return <div>...</div>
  }
  ```

- **re-export は使用しない**
  ```typescript
  // ❌ 避ける
  export { UserProfile } from './user-profile'
  export { Button } from './button'

  // ✅ 必要な場合は直接インポート
  import { UserProfile } from '@/components/user-profile'
  import { Button } from '@/components/button'
  ```

### コンポーネント設計

- **コンポーネントの最上位にマージンをつけない**
  ```typescript
  // ❌ 避ける
  export function Card() {
    return <div className="mt-4 mb-4">...</div>
  }

  // ✅ 推奨
  export function Card() {
    return <div>...</div>
  }

  // 使用側でマージンを制御
  function ParentComponent() {
    return (
      <div>
        <Card className="mt-4 mb-4" />
      </div>
    )
  }
  ```

### データフェッチング

- **getServerSideProps を使用する**
  - ページレベルでサーバーサイドレンダリングが必要な場合に使用
  - リクエストごとにデータを取得する必要がある動的なページに適用

#### getServerSideProps のコーディング規約

1. **変数名の統一**
   - レスポンス変数: `hogeRes` の形式で命名
   - JSON データ変数: `hogeData` の形式で命名
   ```typescript
   // ✅ 推奨
   const userRes = await fetch('/api/user')
   const userData = await userRes.json()

   // ❌ 避ける
   const response = await fetch('/api/user')
   const data = await response.json()
   ```

2. **Context 変数名**
   - Context パラメータは `ctx` を使用する
   ```typescript
   // ✅ 推奨
   export const getServerSideProps: GetServerSideProps = async (ctx) => {
     // ...
   }

   // ❌ 避ける
   export const getServerSideProps: GetServerSideProps = async (context) => {
     // ...
   }
   ```

3. **型解決**
   - `ctx` の型解決は直接行う（型を明示的に指定しない）
   - `params` から動的パラメータを受け取る時は `as string` を使用する
   ```typescript
   export const getServerSideProps: GetServerSideProps = async (ctx) => {
     const { id } = ctx.params as { id: string }
     // または
     const id = ctx.params?.id as string
   }
   ```

4. **エラーハンドリング**
   - GET リクエストで response が 200 でない時は 404 を返す
   ```typescript
   export const getServerSideProps: GetServerSideProps = async (ctx) => {
     const userRes = await fetch(`/api/user/${ctx.params?.id}`)

     if (!userRes.ok) {
       return {
         notFound: true,
       }
     }

     const userData = await userRes.json()

     return {
       props: {
         user: userData,
       },
     }
   }
   ```

5. **型推論の活用**
   - `InferGetServerSidePropsType` を使用して Props の型を推論する
   - default export とページコンポーネントは分ける
   ```typescript
   import { GetServerSideProps, InferGetServerSidePropsType } from 'next'

   export const getServerSideProps: GetServerSideProps = async (ctx) => {
     const id = ctx.params?.id as string
     const userRes = await fetch(`https://api.example.com/users/${id}`)

     if (!userRes.ok) {
       return {
         notFound: true,
       }
     }

     const userData = await userRes.json()

     return {
       props: {
         user: userData,
       },
     }
   }

   // 型推論を使用
   type Props = InferGetServerSidePropsType<typeof getServerSideProps>

   // ページコンポーネントを分けて定義
   function UserPage({ user }: Props) {
     return (
       <div>
         <h1>{user.name}</h1>
       </div>
     )
   }

   // default export は別に定義
   export default UserPage
   ```

6. **完全な実装例**
   ```typescript
   import { GetServerSideProps, InferGetServerSidePropsType } from 'next'

   export const getServerSideProps: GetServerSideProps<{
     user: { id: string; name: string; email: string }
   }> = async (ctx) => {
     const id = ctx.params?.id as string

     // レスポンス変数は hogeRes 形式
     const userRes = await fetch(`https://api.example.com/users/${id}`)

     // 200以外は404を返す
     if (!userRes.ok) {
       return {
         notFound: true,
       }
     }

     // JSONデータは hogeData 形式
     const userData = await userRes.json()

     return {
       props: {
         user: userData,
       },
     }
   }

   // 型推論を活用
   type Props = InferGetServerSidePropsType<typeof getServerSideProps>

   // ページコンポーネントを分けて定義
   function UserDetailPage({ user }: Props) {
     return (
       <div>
         <h1>{user.name}</h1>
         <p>{user.email}</p>
       </div>
     )
   }

   // default export は別に定義
   export default UserDetailPage
   ```

## コードレビュー

### Claude Code による AI レビュー

本プロジェクトでは、**Claude Code を使用した AI レビューを必ず実施する**ことを推奨しています。

#### レビューの実施方法

1. **変更をコミット前にレビュー**
   ```bash
   # Claude Code でレビューを依頼
   # 変更したファイルを開いて、Claude に以下のようにリクエスト
   "この変更をレビューしてください"
   ```

2. **レビュー観点**
   - コーディング規約への準拠
   - 型安全性
   - パフォーマンス
   - アクセシビリティ
   - セキュリティ
   - バグの可能性

3. **レビュー後のアクション**
   - 指摘された問題を修正
   - 必要に応じてコードを改善
   - レビュー内容をチームと共有

## リント・フォーマット

```bash
# ESLint によるリント
npm run lint

# ESLint による自動修正
npm run lint:fix

# Prettier によるフォーマット（自動実行）
# コミット時に自動的に実行されます
```

### Git Hooks

本プロジェクトでは Husky と lint-staged を使用しており、コミット前に自動的にリント・フォーマットが実行されます。

## ディレクトリ構造

```
frontend/
├── src/
│   ├── app/              # Next.js App Router のページ
│   ├── components/       # 再利用可能なコンポーネント
│   ├── lib/              # ユーティリティ関数やヘルパー
│   ├── hooks/            # カスタムフック
│   ├── types/            # TypeScript 型定義
│   └── styles/           # グローバルスタイル
├── public/               # 静的ファイル
└── README.md             # このファイル
```

## 開発のベストプラクティス

1. **型安全性を保つ**
   - `any` 型の使用を避ける
   - 適切な型定義を作成する

2. **コンポーネントの責務を明確にする**
   - 単一責任の原則に従う
   - 小さく再利用可能なコンポーネントを作成する

3. **パフォーマンスを考慮する**
   - 不要な再レンダリングを避ける
   - 画像の最適化（next/image を使用）
   - コード分割を活用する

4. **アクセシビリティを確保する**
   - セマンティックな HTML を使用する
   - ARIA 属性を適切に設定する
   - キーボード操作に対応する

5. **テストを書く**
   - 重要なロジックにはユニットテストを追加
   - ユーザーの主要なフローには E2E テストを追加

## トラブルシューティング

### よくある問題

1. **開発サーバーが起動しない**
   ```bash
   # node_modules を削除して再インストール
   rm -rf node_modules
   npm install
   ```

2. **型エラーが発生する**
   ```bash
   # TypeScript のキャッシュをクリア
   rm -rf .next
   npm run dev
   ```

## 参考リンク

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com)
- [React Documentation](https://react.dev)

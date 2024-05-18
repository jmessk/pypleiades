# PyMEC Client

MECRM API を簡単に扱うことができるライブラリです。

## Features

- `MECAPI`
  - MECRM API の主要なエンドポイント用関数群
  - 実装は最低限
  - このクラスを継承したカスタムクラスを定義することができる
- `MECIO`
  - データやり取り用クラス
  - 内部に `MECAPI` のインスタンスを保持
  - Blob と KV Store を扱う
- `MECRequester`
  - Job を生成し結果を待つ
  - `MECIO` を継承
- `MECWorker`
  - MECRM に Worker を登録する
  - Job を受け取り処理する
  - `MECIO` を継承
- `MECJob`
  - Job に対応
  - `MECRequester` と `MECWorker` により生成される
  - `MECIO` を継承

## Installation

```sh
git clone https://github.com/CREST-applications/pymec-client.git -b main
cd pymec-client
pip3 install -e .
```

## Usage

[`examples`](./examples) を参照

## Todo

- [x] Swagger から生成したコードを使わない実装
- [ ] MECIO クラスに Key-Value store の API を実装
- [x] setuptools でパッケージ化
- [ ] テスト

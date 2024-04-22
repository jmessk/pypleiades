# PyMEC Client

[python-mec-generated](https://github.com/CREST-applications/python-client-generated) をラップして使いやすくしたものです。このライブラリを使用することで、API の変化に対応したクライアントが作成できます。

> [!NOTE]
> 現在は内部で Swagger から生成したコードを使用していません。

## Installation

```sh
git clone https://github.com/CREST-applications/pymec-client.git
cd pymec-client
pip3 install -e .
```

## Usage

[`examples`](./examples) を参照

## Todo

- [x] Swagger から生成したコードを使わない実装
- [ ] MECIO クラスに Key-Value store の API を実装
- [x] setuptools でパッケージ化

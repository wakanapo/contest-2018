STEP Coding Camp 2018 Programming Contest
=========================================

STEP Coding Camp 2018 で行われる Programming Contest で使うプログラムです。ファイル構成は以下のようになっています。

```
+ sample/           : サンプルコードを入れたディレクトリ
| + gomoku.cc
| + Gomoku.java
| + gomoku.py
+ gomoku_server.py  : 対戦用スクリプト
+ README.md         : このファイルです
```

ファイルの説明
============
`sample/`
---------
C/C++、Java、Python のそれぞれで実装されたサンプルコードです。これらのファイルで定義されている `Think()` を改造してもらいます。`Input()`、`Output()`、`main()` は変更しないでください。また、Python のコードでバージョン依存の機能を使う場合は使うバージョンに合わせて 1 行目にある

```
#!/usr/bin/python
```

の末尾 (`python`) を `python2` か `python3` に変更してください。

`gomoku_server.py`
------------------
AI 同士を対戦させるスクリプトです。

```
 $ gomoku_server.py foo/Gomoku.java bar/gomoku
```

のようにプログラムのソースコードもしくは実行ファイル名を 2 つ引数に与えるとそれらを使って対戦してくれます。ソースコードを与えた場合は必要があればコンパイルしてくれます。

# TOC Project 2020
## 前言
每次在玩遊戲的時候都要特地開介面去查詢特定資料有點麻煩，因此做了一個可以查看簡易資料的ChatBot


## Finite State Machine
![fsm](https://i.imgur.com/UMF1uRi.png)

## Usage
初始state為`user`.

連接到兩個分支 `weapon` 和 `monster` 分別對應到武器以及魔物的查詢。

當輸入對應的武器或魔物名稱時，bot會到 [MHW 魔物獵人中文攻略 wiki](http://https://www.mhchinese.wiki/) 抓取相對應的資料

任何時候皆可輸入 `幫助` 或 `指令` 查看說明

## Demo
### Line Bot
![](https://i.imgur.com/nJhM4Y9.png)
### Weapon Search
![](https://i.imgur.com/6XQVxqv.png)
### Monster Search
![](https://i.imgur.com/x8NPSYw.png)
![](https://i.imgur.com/2qc4ioY.png)
### Help State & FSM display
![](https://i.imgur.com/LAjfreo.png)

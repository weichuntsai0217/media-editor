# media-editor
使用moviepy & ffmpeg來剪輯影片和音檔。

# 安裝
建議作業系統為ubuntu，我們使用Python 2.7的環境且必須要先安裝`pipenv`。
請執行下列指令來安裝所有需要的第三方套件
```
$ pipenv install --ignore-pipfile --dev
```

# 安裝注意事項
* 安裝完後，在目錄`~/.imageio/ffmpeg`中會看到`ffmpeg執行檔`，這個執行檔是專門給`moviepy`用的，若沒透過特別設定，其他想用`ffmpeg`的程式是無法用到它的。

* 如果你的`/usr/bin/`中沒有`ffmpeg`，則執行`autosub`和`extract_subtitles.py`和`extract_subtitles_batch.py`都會失敗，這時請你在`/usr/bin/`中建立一個soft link到`~/.imageio/ffmpeg/ffmpeg執行檔`就可以解決問題，例如：假設`ffmpeg執行檔`的檔名為`ffmpeg-linux64-v3.3.1`，且家目錄的名稱為`/home/jimmy`，則請執行以下指令
  ```
  $ cd /usr/bin
  $ ln -s /home/jimmy/.imageio/ffmpeg/ffmpeg-linux64-v3.3.1 ffmpeg
  ```
  這樣`autosub`和`extract_subtitles.py`和`extract_subtitles_batch.py`就可以正常執行。
  當然你也可以考慮直接`apt-get install ffmpeg`在global安裝另一個ffmpeg執行檔也行

# Usage
關於每個python script的用法，請參考每個script的`main` function中最上方的comment.

# 備忘
* 若想單獨執行autosub來產生字幕，請執行
  ```
  $ pipenv run autosub input-video.mp4 -S "zh-TW" -D "zh-TW" -F vtt -o output-subtitles.vtt
  ```
  其中`input-video.mp4`為輸入的影片檔(也可以輸出音訊檔，例如`.mp3`，`.wav`)，`-S "zh-TW"`是設定輸入影片檔的語言(預設是英語)，`-D "zh-TW"`是設定輸出字幕檔的語言，`-F vtt`是設定字幕檔為`vtt`格式(預設是srt)，`-o output-subtitles.vtt`是設定輸出字幕檔的檔名(預設是和輸入影片擁有同樣的主檔名)。

* 若你想要將字幕(subtitles)檔和影片合併成一個影片檔，請執行
  ```
  $ ffmpeg -i input-video.mp4 -vf "subtitles=input-video.vtt:force_style='FontName=AR PL UMing TW,Fontsize=10,PrimaryColour=&Hffffff&,Outline=2,BackColour=&H000000&,BorderStyle=3,Shadow=0,OutlineColour=&H80000000'" output-video.mp4
  ```
  其中`input-video.mp4`為輸入的影片檔，`input-video.vtt`為輸入的字幕檔(`.srt`, `.vtt`都可以)，`output-video.mp4`為輸出的影片檔，`FontName=AR PL UMing TW`這段是設定字體，`Fontsize=10`這段是設定字體大小(預設是`Fontsize=16`)，你的電腦上必須有對應的字體才行。在ubuntu上，可以用`fc-list`來看電腦中安裝了哪些字體。除了`FontName`之外，其他在`force_style`中的設定原則上不要動，出來的字幕應該是白色字且背景是半透明的淺灰色。

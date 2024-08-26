# Please check the file `Supplementary_code_demo.ipynb`

原本打算將程式放在 google colab 讓大家試試看的，不過好像我的程式因為需要額外的視窗顯示而無法執行；
不過講義都已經寫好了，索性放到這裡供人賞閱🙇‍♂️

有興趣的夥伴可以在自己的電腦按以下步驟安裝並嘗試：

1. [安裝 miniconda (或 anaconda)](https://docs.anaconda.com/miniconda/)
2. 打開終端機 (powershell 或 bash 什麼都可以)，輸入以下指令
3. `conda config --add channels conda-forge`
4. `conda create -n general python numpy pandas matplotlib seaborn`
5. `conda create -n opencv python numpy opencv-python`
6. 最後視你要執行的程式需求，透過 `conda activate general` 或 `conda activate opencv` 來切換執行環境 \[ps.\]
8. 當然如果你用 `jupyter lab --notebook-dir=/path/to/your/directory/Supplementary_code_demo.ipynb`，就可以透過 GUI 變更執行環境了。

ps.

- `simple_MS_data_plotter.py` 需要上述 `general` 環境中包含的所有套件才能執行
- `signal_detector_in_roi.py` 則需要在上述 `opencv` 的環境執行
- 當然你可以不分類乾脆全部都裝一起，那麼上述第 4、5 點改成：`conda create -n nppdmplsnscv2 python numpy pandas matplotlib seaborn opencv-python` 就可以了；還是要記得 `conda activate nppdmplsnscv2`

祝大家玩的愉快，希望各位有所收穫~

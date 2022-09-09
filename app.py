import requests
import wx
import wx.lib.buttons as buts
import wx.lib.scrolledpanel as scrolled

from utils import TILES, count_to_tiles, tiles_to_count, YIZHONG
# TODO: data binding
cnt = [0] * len(TILES)


def on_text_change(event):
    global cnt
    new_cnt = tiles_to_count(event.String)
    if new_cnt:
        cnt = new_cnt


def tile_on_click_func(tile_index):
    def on_click(event):
        global cnt

        if sum(cnt) > 14:
            return

        if cnt[tile_index] == 4:
            return
        cnt[tile_index] += 1
        text_ctrl.SetValue(count_to_tiles(cnt))
        if cnt[tile_index] == 4:
            grid_buttons[tile_index].Disable()
        if sum(cnt) == 14:
            for b in grid_buttons:
                b.Enabled = False
            panel.Refresh()

    return on_click


def reset_on_click(event):
    global cnt

    cnt = [0] * len(TILES)
    text_ctrl.Clear()
    for b in grid_buttons:
        b.Enabled = True
    panel.Refresh()


def send_tiles_func(need_interact, reset):
    def send_tiles(event):
        global cnt
        #
        # tiles = text_ctrl.GetValue()
        # _cnt = tiles_to_count(tiles)
        # if not _cnt:
        #     return False
        # cnt = _cnt

        frame_yizhong = wx.Frame(None, title='役种分析结果', size=(w, screen_height - 50), pos=(screen_width - w, 0))
        # panely = wx.Panel(frame_yizhong)
        panely = scrolled.ScrolledPanel(frame_yizhong, -1)

        vboxy = wx.BoxSizer(wx.VERTICAL)

        for jifan in YIZHONG.keys():
            static_text = wx.StaticText(panely, -1, jifan, style=wx.LEFT)
            static_text.SetForegroundColour('red')  # 颜色
            vboxy.Add(static_text, flag=wx.LEFT, border=5)

            for i in range(YIZHONG[jifan]):
                enable_pais = [[1] * 14]

                if jifan=="役满" and i == 0:
                    static_text1 = wx.StaticText(panely, -1, '九莲宝灯', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)

                if jifan=="役满" and i == 1:
                    static_text1 = wx.StaticText(panely, -1, '国士无双', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)

                if jifan=="役满" and i == 2:
                    static_text1 = wx.StaticText(panely, -1, '四暗刻', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                if jifan=="役满" and i == 3:
                    static_text1 = wx.StaticText(panely, -1, '绿一色', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                if jifan=="役满" and i == 4:
                    static_text1 = wx.StaticText(panely, -1, '字一色', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                if jifan=="役满" and i == 5:
                    static_text1 = wx.StaticText(panely, -1, '小四喜', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                if jifan=="役满" and i == 6:
                    static_text1 = wx.StaticText(panely, -1, '清老头', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                if jifan=="役满" and i == 7:
                    static_text1 = wx.StaticText(panely, -1, '四杠子', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                if jifan=="役满" and i == 8:
                    static_text1 = wx.StaticText(panely, -1, '大三元', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)


                if jifan=="双倍役满" and i == 0:
                    static_text1 = wx.StaticText(panely, -1, '大四喜', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)


                if jifan=="六番" and i == 0:
                    static_text1 = wx.StaticText(panely, -1, '清一色', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)

                if jifan=="三番" and i == 0:
                    static_text1 = wx.StaticText(panely, -1, '混一色', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                if jifan=="三番" and i == 1:
                    static_text1 = wx.StaticText(panely, -1, '纯全带幺九', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                if jifan=="三番" and i == 2:
                    static_text1 = wx.StaticText(panely, -1, '二杯口', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)


                if jifan=="二番" and i == 0:
                    static_text1 = wx.StaticText(panely, -1, '小三元', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                if jifan=="二番" and i == 1:
                    static_text1 = wx.StaticText(panely, -1, '三杠子', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                if jifan=="二番" and i == 2:
                    static_text1 = wx.StaticText(panely, -1, '混老头', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                if jifan=="二番" and i == 3:
                    static_text1 = wx.StaticText(panely, -1, '三暗刻', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                if jifan=="二番" and i == 4:
                    static_text1 = wx.StaticText(panely, -1, '对对和', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                if jifan=="二番" and i == 5:
                    static_text1 = wx.StaticText(panely, -1, '三色同刻', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                if jifan=="二番" and i == 6:
                    static_text1 = wx.StaticText(panely, -1, '三色同顺', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                if jifan=="二番" and i == 7:
                    static_text1 = wx.StaticText(panely, -1, '混全带幺九', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                if jifan=="二番" and i == 8:
                    static_text1 = wx.StaticText(panely, -1, '一气通贯', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                if jifan=="二番" and i == 9:
                    static_text1 = wx.StaticText(panely, -1, '七对子', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)


                if jifan=="一番" and i == 0:
                    static_text1 = wx.StaticText(panely, -1, '段幺九', style=wx.LEFT)
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)

                for enable_pai in enable_pais:
                    grid_sizery = wx.GridSizer(1, 14, 4, 4)
                    grid_buttonsy = []
                    for index, tile in enumerate(cnt):
                        for z in range(tile):
                            path = f'img_small/{TILES[index]}.png'
                            button = buts.GenBitmapTextButton(panely, -1, size=(24, 20), bitmap=wx.Bitmap(path))
                            grid_sizery.Add(button, flag=wx.LEFT, border=5)
                            grid_buttonsy.append(button)
                    for j, but in enumerate(grid_buttonsy):
                        if enable_pai[j] == 0:
                            grid_buttonsy[j].Disable()
                    vboxy.Add(grid_sizery, flag=wx.LEFT, border=5)

        panely.SetSizer(vboxy)
        panely.SetupScrolling()

        frame_yizhong.Show()

        ##reset
        cnt = [0] * len(TILES)
        text_ctrl.Clear()
        for i, b in enumerate(grid_buttons):
            b.Enabled = cnt[i] < 4

        panel.Refresh()

        return True

    return send_tiles


if __name__ == '__main__':
    app = wx.App()

    # 默认显示在屏幕右下
    w, h = 600, 480
    screen_width, screen_height = wx.GetDisplaySize()
    frame = wx.Frame(None, title='日麻役种分析', size=(w, h), pos=(screen_width - w, screen_height - h))
    panel = wx.Panel(frame)

    # TODO: 撤销按钮

    text_ctrl = wx.TextCtrl(panel)
    frame.Bind(wx.EVT_TEXT, on_text_change, text_ctrl)

    reset_button = wx.Button(panel, label='重置')
    reset_button.Bind(wx.EVT_BUTTON, reset_on_click)

    hbox = wx.BoxSizer()
    hbox.Add(text_ctrl, proportion=3, flag=wx.EXPAND)
    hbox.Add(reset_button, proportion=1, flag=wx.EXPAND, border=5)

    grid_sizer = wx.GridSizer(4, 9, 4, 4)

    grid_buttons = []
    for index, tile in enumerate(TILES):
        path = f'img/{tile}.png'
        button = buts.GenBitmapTextButton(panel, -1, bitmap=wx.Bitmap(path))
        button.Bind(wx.EVT_BUTTON, tile_on_click_func(index))
        grid_sizer.Add(button, proportion=1, flag=wx.EXPAND, border=5)
        grid_buttons.append(button)

    analysis_button = wx.Button(panel, label='分析')
    analysis_button.Bind(wx.EVT_BUTTON, send_tiles_func(False, True))
    grid_sizer.Add(analysis_button, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

    vbox = wx.BoxSizer(wx.VERTICAL)
    vbox.Add(hbox, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
    vbox.Add(grid_sizer, proportion=4, flag=wx.EXPAND | wx.ALL, border=5)
    panel.SetSizer(vbox)

    frame.Show()

    app.MainLoop()

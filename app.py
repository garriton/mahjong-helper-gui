import wx
import wx.lib.buttons as buts
import wx.lib.scrolledpanel as scrolled
import copy
import os

#from utils import TILES, count_to_tiles, tiles_to_count, YIZHONG
TILES = [
    "1m", "2m", "3m", "4m", "5m", "6m", "7m", "8m", "9m",
    "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p",
    "1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s",
    "1z", "2z", "3z", "4z", "5z", "6z", "7z",
]

YIZHONG = {
    "役满": 9,
    "双倍役满": 1,
    "六番": 1,
    "三番": 3,
    "二番": 10,
    "一番": 1,
}


def count_to_tiles(cnt):
    if len(cnt) != len(TILES):
        print("cnt 长度必须为", len(TILES))
        return ""

    tiles = ""
    for i, type_ in enumerate(['m', 'p', 's', 'z']):
        wrote = False
        for j in range(9):
            idx = 9 * i + j
            if idx >= len(TILES):
                break
            for k in range(cnt[idx]):
                tiles += str(j + 1)
                wrote = True
        if wrote:
            tiles += type_ + " "
    return tiles.strip()


def tiles_to_count(tiles):
    tiles = tiles.strip()
    if tiles == "":
        return []

    cnt = [0] * len(TILES)

    for split in tiles.split():
        split = split.strip()
        if len(split) <= 1:
            print("参数错误:", split)
            return []
        for c in split[:-1]:
            tile = c + split[-1]
            try:
                index = TILES.index(tile)
            except ValueError:
                print("参数错误:", tile)
                return []
            cnt[index] += 1
            if cnt[index] > 4:
                print("参数错误: 超过4张一样的牌")
                return []

    return cnt

# TODO: data binding
cnt = [0] * len(TILES)

paitypes = ["m", "p", "s", "z"]

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
    global cnt, pais, daojigele

    cnt = [0] * len(TILES)
    text_ctrl.Clear()
    for b in grid_buttons:
        b.Enabled = True
    panel.Refresh()

def zhaopaixing(ipai, shangyi_cnt, shangyipx, paixing, ispaixing, paitype, daojigele):
    global cnt
    if (paitype != 3 and ipai == 9) or (paitype == 3 and ipai == 7):
        for indexpai, shangyicnt in enumerate(shangyi_cnt[:-1]):
            if shangyicnt != 0:
                ispaixing = True
                if shangyicnt == 1:
                    shangyipx["meiyong"].append((str(indexpai + 1), sum(cnt[:paitype * 9 + indexpai]) + (cnt[paitype * 9 + indexpai] - shangyi_cnt[indexpai])))
                    shangyi_cnt[indexpai] = shangyi_cnt[indexpai] - 1
                if shangyicnt == 2:
                    shangyipx["duizi"].append((str(indexpai + 1) + str(indexpai + 1), sum(cnt[:paitype * 9 + indexpai]) + (cnt[paitype * 9 + indexpai] - shangyi_cnt[indexpai])))
                    shangyi_cnt[indexpai] = shangyi_cnt[indexpai] - 2
                if shangyicnt == 3:
                    shangyipx["kezi"].append((str(indexpai + 1) + str(indexpai + 1) + str(indexpai + 1), sum(cnt[:paitype * 9 + indexpai]) + (cnt[paitype * 9 + indexpai] - shangyi_cnt[indexpai])))
                    shangyi_cnt[indexpai] = shangyi_cnt[indexpai] - 3
                if shangyicnt == 4:
                    shangyipx["gangzi"].append((
                        str(indexpai + 1) + str(indexpai + 1) + str(indexpai + 1) + str(indexpai + 1), sum(cnt[:paitype * 9 + indexpai]) + (cnt[paitype * 9 + indexpai] - shangyi_cnt[indexpai])))
                    shangyi_cnt[indexpai] = shangyi_cnt[indexpai] - 4
        if ispaixing:
            paixing[paitypes[paitype]].append(shangyipx)
        return
    else:
        if shangyi_cnt[ipai] == 0:
            zhaopaixing(ipai + 1, shangyi_cnt, shangyipx, paixing, ispaixing, paitype, daojigele + cnt[paitype * 9 + ipai])
        else:
            ispaixing = True
        isshunzi = False
        if shangyi_cnt[ipai] >= 1 and paitype != 3:
            isshunzi = False
            # TODO  顺子应该笛卡尔积
            if ipai > 1 and shangyi_cnt[ipai - 2] != 0 and shangyi_cnt[ipai - 1] != 0:
                isshunzi = True
                shangyipx_cp = copy.deepcopy(shangyipx)
                # shunzi_count = (shangyi_cnt[ipai - 2] + shangyi_cnt[ipai - 1] + shangyi_cnt[ipai]) // 3
                shangyipx_cp["shunzi"].append((str(ipai - 2 + 1) + str(ipai - 1 + 1) + str(ipai + 1),
                                            [daojigele - cnt[paitype * 9 + ipai - 1] - shangyi_cnt[ipai - 2],
                                             daojigele - shangyi_cnt[ipai - 1],
                                             daojigele + (cnt[paitype * 9 + ipai] - shangyi_cnt[ipai])]))
                shangyi_cnt_cp = copy.deepcopy(shangyi_cnt)
                shangyi_cnt_cp[ipai] = shangyi_cnt_cp[ipai] - 1
                shangyi_cnt_cp[ipai - 2] = shangyi_cnt_cp[ipai - 2] - 1
                shangyi_cnt_cp[ipai - 1] = shangyi_cnt_cp[ipai - 1] - 1
                zhaopaixing(ipai + 1, shangyi_cnt_cp, shangyipx_cp, paixing, ispaixing, paitype, daojigele + cnt[paitype * 9 + ipai])
            if 8 > ipai > 0 and shangyi_cnt[ipai - 1] != 0 and shangyi_cnt[ipai + 1] != 0:
                isshunzi = True
                shangyipx_cp = copy.deepcopy(shangyipx)
                shangyipx_cp["shunzi"].append((str(ipai - 1 + 1) + str(ipai + 1) + str(ipai + 1 + 1),
                                            [daojigele - shangyi_cnt[ipai - 1],
                                             daojigele + (cnt[paitype * 9 + ipai] - shangyi_cnt[ipai]),
                                             daojigele + cnt[paitype * 9 + ipai] + (cnt[paitype * 9 + ipai + 1] - shangyi_cnt[ipai + 1])]))
                shangyi_cnt_cp = copy.deepcopy(shangyi_cnt)
                shangyi_cnt_cp[ipai] = shangyi_cnt_cp[ipai] - 1
                shangyi_cnt_cp[ipai - 1] = shangyi_cnt_cp[ipai - 1] - 1
                shangyi_cnt_cp[ipai + 1] = shangyi_cnt_cp[ipai + 1] - 1
                zhaopaixing(ipai + 1, shangyi_cnt_cp, shangyipx_cp, paixing, ispaixing, paitype, daojigele + cnt[paitype * 9 + ipai])
            if ipai < 7 and shangyi_cnt[ipai + 1] != 0 and shangyi_cnt[ipai + 2] != 0:
                isshunzi = True
                shangyipx_cp = copy.deepcopy(shangyipx)
                shangyipx_cp["shunzi"].append((str(ipai + 1) + str(ipai + 1 + 1) + str(ipai + 2 + 1),
                                            [daojigele + (cnt[paitype * 9 + ipai] - shangyi_cnt[ipai]),
                                             daojigele + cnt[paitype * 9 + ipai] + (cnt[paitype * 9 + ipai + 1] - shangyi_cnt[ipai + 1]),
                                             daojigele + cnt[paitype * 9 + ipai] + cnt[paitype * 9 + ipai + 1] + (cnt[paitype * 9 + ipai + 2] - shangyi_cnt[ipai + 2])]))
                shangyi_cnt_cp = copy.deepcopy(shangyi_cnt)
                shangyi_cnt_cp[ipai] = shangyi_cnt_cp[ipai] - 1
                shangyi_cnt_cp[ipai + 1] = shangyi_cnt_cp[ipai + 1] - 1
                shangyi_cnt_cp[ipai + 2] = shangyi_cnt_cp[ipai + 2] - 1
                zhaopaixing(ipai + 1, shangyi_cnt_cp, shangyipx_cp, paixing, ispaixing, paitype, daojigele + cnt[paitype * 9 + ipai])
        if shangyi_cnt[ipai] >= 2:
            shangyipx_cp = copy.deepcopy(shangyipx)
            shangyipx_cp["duizi"].append((str(ipai + 1) + str(ipai + 1), daojigele + (cnt[paitype * 9 + ipai] - shangyi_cnt[ipai])))
            shangyi_cnt_cp = copy.deepcopy(shangyi_cnt)
            shangyi_cnt_cp[ipai] = shangyi_cnt_cp[ipai] - 2
            if shangyi_cnt_cp[ipai] == 1:
                shangyipx_cp["meiyong"].append((str(ipai + 1), daojigele + (cnt[paitype * 9 + ipai] - shangyi_cnt_cp[ipai])))
                shangyi_cnt_cp[ipai] = shangyi_cnt_cp[ipai] - 1
            if shangyi_cnt_cp[ipai] == 2:
                shangyipx_cp["duizi"].append((str(ipai + 1) + str(ipai + 1), daojigele + (cnt[paitype * 9 + ipai] - shangyi_cnt_cp[ipai])))
                shangyi_cnt_cp[ipai] = shangyi_cnt_cp[ipai] - 2
            zhaopaixing(ipai + 1, shangyi_cnt_cp, shangyipx_cp, paixing, ispaixing, paitype, daojigele + cnt[paitype * 9 + ipai])
        if shangyi_cnt[ipai] >= 3:
            shangyipx_cp = copy.deepcopy(shangyipx)
            shangyipx_cp["kezi"].append((str(ipai + 1) + str(ipai + 1) + str(ipai + 1), daojigele + (cnt[paitype * 9 + ipai] - shangyi_cnt[ipai])))
            shangyi_cnt_cp = copy.deepcopy(shangyi_cnt)
            shangyi_cnt_cp[ipai] = shangyi_cnt_cp[ipai] - 3
            if shangyi_cnt_cp[ipai] == 1:
                shangyipx_cp["meiyong"].append((str(ipai + 1), daojigele + (cnt[paitype * 9 + ipai] - shangyi_cnt_cp[ipai])))
                shangyi_cnt_cp[ipai] = shangyi_cnt_cp[ipai] - 1
            zhaopaixing(ipai + 1, shangyi_cnt_cp, shangyipx_cp, paixing, ispaixing, paitype, daojigele + cnt[paitype * 9 + ipai])
        if shangyi_cnt[ipai] >= 4:
            shangyipx_cp = copy.deepcopy(shangyipx)
            shangyipx_cp["gangzi"].append((str(ipai + 1) + str(ipai + 1) + str(ipai + 1) + str(ipai + 1), daojigele + (cnt[paitype * 9 + ipai] - shangyi_cnt[ipai])))
            shangyi_cnt_cp = copy.deepcopy(shangyi_cnt)
            shangyi_cnt_cp[ipai] = shangyi_cnt_cp[ipai] - 4
            zhaopaixing(ipai + 1, shangyi_cnt_cp, shangyipx_cp, paixing, ispaixing, paitype, daojigele + cnt[paitype * 9 + ipai])
        if shangyi_cnt[ipai] == 1:
            shangyipx_cp = copy.deepcopy(shangyipx)
            shangyipx_cp["meiyong"].append((str(ipai + 1), daojigele + (cnt[paitype * 9 + ipai] - shangyi_cnt[ipai])))
            shangyi_cnt_cp = copy.deepcopy(shangyi_cnt)
            shangyi_cnt_cp[ipai] = shangyi_cnt_cp[ipai] - 1
            zhaopaixing(ipai + 1, shangyi_cnt_cp, shangyipx_cp, paixing, ispaixing, paitype, daojigele + cnt[paitype * 9 + ipai])


def zhaosuoyoukezi(paixindex, paixing, suoyoukezi, suoyoukezis):
    if paixindex == 4:
        if len(suoyoukezi):
            suoyoukezis.append(suoyoukezi)
        return
    if len(paixing[paitypes[paixindex]]) != 0:
        for pxkezi in paixing[paitypes[paixindex]]:
            suoyoukezi_cp = copy.deepcopy(suoyoukezi)
            suoyoukezi_cp = suoyoukezi_cp + pxkezi["kezi"]
            zhaosuoyoukezi(paixindex + 1, paixing, suoyoukezi_cp, suoyoukezis)
    else:
        suoyoukezi_cp = copy.deepcopy(suoyoukezi)
        zhaosuoyoukezi(paixindex + 1, paixing, suoyoukezi_cp, suoyoukezis)

def zhaosuoyougangzi(paixindex, paixing, suoyougangzi, suoyougangzis):
    if paixindex == 4:
        if len(suoyougangzi):
            suoyougangzis.append(suoyougangzi)
        return
    if len(paixing[paitypes[paixindex]]) != 0:
        for pxkezi in paixing[paitypes[paixindex]]:
            suoyougangzi_cp = copy.deepcopy(suoyougangzi)
            suoyougangzi_cp = suoyougangzi_cp + pxkezi["gangzi"]
            zhaosuoyougangzi(paixindex + 1, paixing, suoyougangzi_cp, suoyougangzis)
    else:
        suoyougangzi_cp = copy.deepcopy(suoyougangzi)
        zhaosuoyougangzi(paixindex + 1, paixing, suoyougangzi_cp, suoyougangzis)
        
def zhaosuoyouduizi(paixindex, paixing, suoyouduizi, suoyouduizis):
    if paixindex == 4:
        if len(suoyouduizi):
            suoyouduizis.append(suoyouduizi)
        return
    if len(paixing[paitypes[paixindex]]) != 0:
        for pxkezi in paixing[paitypes[paixindex]]:
            suoyouduizi_cp = copy.deepcopy(suoyouduizi)
            suoyouduizi_cp = suoyouduizi_cp + pxkezi["duizi"]
            zhaosuoyouduizi(paixindex + 1, paixing, suoyouduizi_cp, suoyouduizis)
    else:
        suoyouduizi_cp = copy.deepcopy(suoyouduizi)
        zhaosuoyouduizi(paixindex + 1, paixing, suoyouduizi_cp, suoyouduizis)

def zhaosuoyoushunzi(paixindex, paixing, suoyoushunzi, suoyoushunzis):
    if paixindex == 4:
        if len(suoyoushunzi):
            suoyoushunzis.append(suoyoushunzi)
        return
    if len(paixing[paitypes[paixindex]]) != 0:
        for pxkezi in paixing[paitypes[paixindex]]:
            suoyoushunzi_cp = copy.deepcopy(suoyoushunzi)
            suoyoushunzi_cp = suoyoushunzi_cp + pxkezi["shunzi"]
            zhaosuoyoushunzi(paixindex + 1, paixing, suoyoushunzi_cp, suoyoushunzis)
    else:
        suoyoushunzi_cp = copy.deepcopy(suoyoushunzi)
        zhaosuoyoushunzi(paixindex + 1, paixing, suoyoushunzi_cp, suoyoushunzis)

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
                enable_pais = []
                pais = {
                    "m": [],
                    "p": [],
                    "s": [],
                    "z": []
                }

                paixing = {
                    "m": [],
                    "p": [],
                    "s": [],
                    "z": []
                }

                m_cnt = cnt[0:9]
                p_cnt = cnt[9:18]
                s_cnt = cnt[18:27]
                z_cnt = cnt[27:34]
                z_cnt.append(0)
                z_cnt.append(0)

                cnt_copy = [m_cnt, p_cnt, s_cnt, z_cnt]

                for ipaitype, i_cnt in enumerate(cnt_copy):
                    shangyipx = {
                        "duizi": [],
                        "kezi": [],
                        "gangzi": [],
                        "shunzi": [],
                        "meiyong": []
                    }
                    for title_index, title_num in enumerate(i_cnt):
                        for itnum in range(title_num):
                            pais[paitypes[ipaitype]].append(title_index)
                    zhaopaixing(0, i_cnt, shangyipx, paixing, False, ipaitype, sum(cnt[:ipaitype * 9]))

                cnt_copy = [m_cnt, p_cnt, s_cnt, z_cnt]


                if jifan=="役满" and i == 0:
                    static_text1 = wx.StaticText(panely, -1, '九莲宝灯', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '同种数牌1112345678999+其中任意一种再有1张', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    daolenagepai = 0
                    paitype = 0
                    shifoujiulianbaodeng = False
                    for tongyipainame in pais:
                        if paitype == 3:
                            break
                        paitype += 1
                        tongyipai = pais[tongyipainame]
                        jiulianjishu = [3, 1, 1, 1, 1, 1, 1, 1, 1, 3]
                        enable_pai = [0] * sum(cnt)
                        shifouyoupai = False
                        for paiindex, objpai in enumerate(tongyipai):
                            shifouyoupai = True
                            if jiulianjishu[objpai % 9] != 0:
                                jiulianjishu[objpai % 9] -= 1
                                enable_pai[daolenagepai] = 1
                            daolenagepai += 1
                        if shifouyoupai:
                            shifoujiulianbaodeng = True
                            enable_pais.append(enable_pai)
                    if not shifoujiulianbaodeng:
                        enable_pai = [0] * sum(cnt)
                        enable_pais.append(enable_pai)

                if jifan=="役满" and i == 1:
                    static_text1 = wx.StaticText(panely, -1, '国士无双', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '全部十三种幺九牌各1张外加其中一种再有1张', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    guoshijishu = [1, 0, 0, 0, 0, 0, 0, 0, 1] * 3 + [1, 1, 1, 1, 1, 1, 1, 0, 0]
                    enable_pai = [0] * sum(cnt)
                    daolenagepai = 0
                    paitype = 0
                    for tongyipainame in pais:
                        tongyipai = pais[tongyipainame]
                        for paiindex, objpai in enumerate(tongyipai):
                            if guoshijishu[paitype * 9 + objpai] != 0:
                                guoshijishu[paitype * 9 + objpai] -= 1
                                enable_pai[daolenagepai] = 1
                            daolenagepai += 1
                        paitype += 1
                    enable_pais.append(enable_pai)

                if jifan=="役满" and i == 2:
                    static_text1 = wx.StaticText(panely, -1, '四暗刻', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '包含没有碰的4组刻子', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    enable_pai = [0] * sum(cnt)
                    max_kezi = 0
                    max_kezi_index = []
                    suoyoukezis = []
                    zhaosuoyoukezi(0, paixing, [], suoyoukezis)
                    for kezis in suoyoukezis:
                        if max_kezi < len(kezis):
                            max_kezi = len(kezis)
                            max_kezi_index = kezis
                    for kezi, keziindex in max_kezi_index:
                        enable_pai[keziindex] = 1
                        enable_pai[keziindex + 1] = 1
                        enable_pai[keziindex + 2] = 1
                    enable_pais.append(enable_pai)

                if jifan=="役满" and i == 3:
                    static_text1 = wx.StaticText(panely, -1, '绿一色', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '只包含索子的23468以及发', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    enable_pai = [0] * sum(cnt)
                    daolenagepai = len(pais["m"]) + len(pais["p"])
                    for paiindex, objpai in enumerate(pais["s"]):
                        if objpai != 0 and objpai != 4 and objpai != 6 and objpai != 8:
                            enable_pai[daolenagepai] = 1
                        daolenagepai += 1
                    for paiindex, objpai in enumerate(pais["z"]):
                        if objpai == 5:
                            enable_pai[daolenagepai] = 1
                        daolenagepai += 1
                    enable_pais.append(enable_pai)

                if jifan=="役满" and i == 4:
                    static_text1 = wx.StaticText(panely, -1, '字一色', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '只包含字牌', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    enable_pai = [0] * sum(cnt)
                    daolenagepai = len(pais["m"]) + len(pais["p"]) + len(pais["s"])
                    for paiindex, objpai in enumerate(pais["z"]):
                        enable_pai[daolenagepai] = 1
                        daolenagepai += 1
                    enable_pais.append(enable_pai)

                if jifan=="役满" and i == 5:
                    static_text1 = wx.StaticText(panely, -1, '小四喜', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '包含三种风牌的刻子+剩下一种风牌的雀头', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    enable_pai = [0] * sum(cnt)
                    daolenagepai = len(pais["m"]) + len(pais["p"]) + len(pais["s"])
                    fengpaijishu = [3, 3, 3, 3, 0, 0, 0, 0, 0]
                    for paiindex, objpai in enumerate(pais["z"]):
                        if objpai < 4 and fengpaijishu[objpai] != 0:
                            fengpaijishu[objpai] -= 1
                            enable_pai[daolenagepai] = 1
                        daolenagepai += 1
                    enable_pais.append(enable_pai)


                if jifan=="役满" and i == 6:
                    static_text1 = wx.StaticText(panely, -1, '清老头', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '手牌中只有老头牌(19万，19筒，19索)', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    daolenagepai = 0
                    paitype = 0
                    enable_pai = [0] * sum(cnt)
                    for tongyipainame in pais:
                        if paitype == 3:
                            break
                        tongyipai = pais[tongyipainame]
                        for paiindex, objpai in enumerate(tongyipai):
                            if objpai == 0 or objpai == 8:
                                enable_pai[daolenagepai] = 1
                            daolenagepai += 1
                        paitype += 1
                    enable_pais.append(enable_pai)

                if jifan=="役满" and i == 7:
                    static_text1 = wx.StaticText(panely, -1, '四杠子', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '1人开杠4次', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    enable_pai = [0] * sum(cnt)
                    max_gangzi = 0
                    max_gangzi_index = []
                    suoyougangzis = []
                    zhaosuoyougangzi(0, paixing, [], suoyougangzis)
                    for gangzis in suoyougangzis:
                        if max_gangzi < len(gangzis):
                            max_gangzi = len(gangzis)
                            max_gangzi_index = gangzis
                    for gangzi, gangziindex in max_gangzi_index:
                        enable_pai[gangziindex] = 1
                        enable_pai[gangziindex + 1] = 1
                        enable_pai[gangziindex + 2] = 1
                        enable_pai[gangziindex + 3] = 1
                    enable_pais.append(enable_pai)

                if jifan=="役满" and i == 8:
                    static_text1 = wx.StaticText(panely, -1, '大三元', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '包含白、发、中的三组刻子', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    enable_pai = [0] * sum(cnt)
                    daolenagepai = len(pais["m"]) + len(pais["p"]) + len(pais["s"])
                    fengpaijishu = [0, 0, 0, 0, 3, 3, 3, 0, 0]
                    for paiindex, objpai in enumerate(pais["z"]):
                        if 7 > objpai > 3 and fengpaijishu[objpai] != 0:
                            fengpaijishu[objpai] -= 1
                            enable_pai[daolenagepai] = 1
                        daolenagepai += 1
                    enable_pais.append(enable_pai)


                if jifan=="双倍役满" and i == 0:
                    static_text1 = wx.StaticText(panely, -1, '大四喜', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '包含4种风牌的刻子', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    enable_pai = [0] * sum(cnt)
                    daolenagepai = len(pais["m"]) + len(pais["p"]) + len(pais["s"])
                    fengpaijishu = [3, 3, 3, 3, 0, 0, 0, 0, 0]
                    for paiindex, objpai in enumerate(pais["z"]):
                        if objpai < 4 and fengpaijishu[objpai] != 0:
                            fengpaijishu[objpai] -= 1
                            enable_pai[daolenagepai] = 1
                        daolenagepai += 1
                    enable_pais.append(enable_pai)


                if jifan=="六番" and i == 0:
                    static_text1 = wx.StaticText(panely, -1, '清一色', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '只包含1种数牌，不能含有字牌', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    daolenagepai = 0
                    paitype = 0
                    shifouqingyise = False
                    for tongyipainame in pais:
                        if paitype == 3:
                            break
                        paitype += 1
                        tongyipai = pais[tongyipainame]
                        enable_pai = [0] * sum(cnt)
                        shifouyoupai = False
                        for paiindex, objpai in enumerate(tongyipai):
                            shifouyoupai = True
                            enable_pai[daolenagepai] = 1
                            daolenagepai += 1
                        if shifouyoupai:
                            shifouqingyise = True
                            enable_pais.append(enable_pai)
                    if not shifouqingyise:
                        enable_pai = [0] * sum(cnt)
                        enable_pais.append(enable_pai)


                if jifan=="三番" and i == 0:
                    static_text1 = wx.StaticText(panely, -1, '混一色', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '只包含1种数牌，并且含有字牌的刻子或者雀头', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    daolenagepai = 0
                    paitype = 0
                    shifouqingyise = False
                    for tongyipainame in pais:
                        if paitype == 3:
                            break
                        paitype += 1
                        tongyipai = pais[tongyipainame]
                        enable_pai = [0] * sum(cnt)
                        shifouyoupai = False
                        for paiindex, objpai in enumerate(tongyipai):
                            shifouyoupai = True
                            enable_pai[daolenagepai] = 1
                            daolenagepai += 1
                        zipaijishu = [3, 3, 3, 3, 3, 3, 3, 0, 0]
                        zipaidaolenagepai = len(pais["m"]) + len(pais["p"]) + len(pais["s"])
                        for paiindex, objpai in enumerate(pais["z"]):
                            if zipaijishu[objpai] != 0:
                                zipaijishu[objpai] -= 1
                                enable_pai[zipaidaolenagepai] = 1
                            zipaidaolenagepai += 1
                        if shifouyoupai:
                            shifouqingyise = True
                            enable_pais.append(enable_pai)
                    if not shifouqingyise:
                        enable_pai = [0] * sum(cnt)
                        enable_pais.append(enable_pai)

                if jifan=="三番" and i == 1:
                    static_text1 = wx.StaticText(panely, -1, '纯全带幺九', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '只包含老头牌的4组顺子和刻子+老头牌的雀头', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    enable_pai = [0] * sum(cnt)
                    for pxstr in paixing:
                        if pxstr == "z":
                            continue
                        max_laotoupai = 0
                        max_enable_pais = [0] * sum(cnt)
                        for pxdict in paixing[pxstr]:
                            temp_max_laotoupai = 0
                            temp_enable_pais = [0] * sum(cnt)
                            laotoujishu = [3, 0, 0, 0, 0, 0, 0, 0, 3]
                            for laotoushunzi, laotoushunziindex in pxdict["shunzi"]:
                                if laotoushunzi[0] == "1" or laotoushunzi[2] == "9":
                                    temp_max_laotoupai += 3
                                    for laotouenablepai in laotoushunziindex:
                                        temp_enable_pais[laotouenablepai] = 1
                            for laotoushunzi, laotoushunziindex in pxdict["kezi"]:
                                if laotoushunzi[0] == "1" or laotoushunzi[0] == "9":
                                    temp_max_laotoupai += 3
                                    temp_enable_pais[laotoushunziindex] = 1
                                    temp_enable_pais[laotoushunziindex + 1] = 1
                                    temp_enable_pais[laotoushunziindex + 2] = 1
                            for laotoushunzi, laotoushunziindex in pxdict["duizi"]:
                                if (laotoushunzi[0] == "1" or laotoushunzi[0] == "9") and laotoujishu[int(laotoushunzi[0]) - 1] > 0:
                                    temp_max_laotoupai += 2
                                    temp_enable_pais[laotoushunziindex] = 1
                                    temp_enable_pais[laotoushunziindex + 1] = 1
                                    laotoujishu[int(laotoushunzi[0]) - 1] -= 2
                            for laotoushunzi, laotoushunziindex in pxdict["meiyong"]:
                                if (laotoushunzi[0] == "1" or laotoushunzi[0] == "9") and laotoujishu[int(laotoushunzi[0]) - 1] > 0:
                                    temp_max_laotoupai += 1
                                    temp_enable_pais[laotoushunziindex] = 1
                                    laotoujishu[int(laotoushunzi[0]) - 1] -= 2
                            if temp_max_laotoupai > max_laotoupai:
                                max_laotoupai = temp_max_laotoupai
                                max_enable_pais = temp_enable_pais
                        for laotouindex, laotpuenable in enumerate(max_enable_pais):
                            if laotpuenable:
                                enable_pai[laotouindex] = 1
                    enable_pais.append(enable_pai)

                if jifan=="三番" and i == 2:
                    static_text1 = wx.StaticText(panely, -1, '二杯口', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '包含2组一杯口', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    enable_pai = [0] * sum(cnt)
                    paitype = 0
                    for pxstr in paixing:
                        if pxstr == "z":
                            continue
                        max_laotoupai = 0
                        max_enable_pais = [0] * sum(cnt)
                        for pxdict in paixing[pxstr]:
                            temp_max_laotoupai = 0
                            temp_enable_pais = [0] * sum(cnt)
                            laotoujishu = [3, 0, 0, 0, 0, 0, 0, 0, 3]
                            for laotoushunzi, laotoushunziindex in pxdict["shunzi"]:
                                if cnt_copy[paitype][int(laotoushunzi[0]) - 1] > 1 or cnt_copy[paitype][int(laotoushunzi[1]) - 1] > 1 or cnt_copy[paitype][int(laotoushunzi[2]) - 1] > 1:
                                    temp_max_laotoupai += 3
                                    for laotouenablepai in laotoushunziindex:
                                        temp_enable_pais[laotouenablepai] = 1
                                    if cnt_copy[paitype][int(laotoushunzi[0]) - 1] > 1:
                                        temp_max_laotoupai += 1
                                        temp_enable_pais[laotoushunziindex[0] + 1] = 1
                                    if cnt_copy[paitype][int(laotoushunzi[1]) - 1] > 1:
                                        temp_max_laotoupai += 1
                                        temp_enable_pais[laotoushunziindex[1] + 1] = 1
                                    if cnt_copy[paitype][int(laotoushunzi[2]) - 1] > 1:
                                        temp_max_laotoupai += 1
                                        temp_enable_pais[laotoushunziindex[2] + 1] = 1
                            if temp_max_laotoupai > max_laotoupai:
                                max_laotoupai = temp_max_laotoupai
                                max_enable_pais = temp_enable_pais
                        for laotouindex, laotpuenable in enumerate(max_enable_pais):
                            if laotpuenable:
                                enable_pai[laotouindex] = 1
                        paitype += 1
                    enable_pais.append(enable_pai)


                if jifan=="二番" and i == 0:
                    static_text1 = wx.StaticText(panely, -1, '小三元', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '包含白、发、中其中2种的刻子+剩下1种的雀头', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    enable_pai = [0] * sum(cnt)
                    daolenagepai = len(pais["m"]) + len(pais["p"]) + len(pais["s"])
                    fengpaijishu = [0, 0, 0, 0, 3, 3, 3, 0, 0]
                    for paiindex, objpai in enumerate(pais["z"]):
                        if 7 > objpai > 3 and fengpaijishu[objpai] != 0:
                            fengpaijishu[objpai] -= 1
                            enable_pai[daolenagepai] = 1
                        daolenagepai += 1
                    enable_pais.append(enable_pai)

                if jifan=="二番" and i == 1:
                    static_text1 = wx.StaticText(panely, -1, '三杠子', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '一人开杠3次', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    enable_pai = [0] * sum(cnt)
                    max_gangzi = 0
                    max_gangzi_index = []
                    suoyougangzis = []
                    zhaosuoyougangzi(0, paixing, [], suoyougangzis)
                    for gangzis in suoyougangzis:
                        if max_gangzi < len(gangzis):
                            max_gangzi = len(gangzis)
                            max_gangzi_index = gangzis
                    for gangzi, gangziindex in max_gangzi_index:
                        enable_pai[gangziindex] = 1
                        enable_pai[gangziindex + 1] = 1
                        enable_pai[gangziindex + 2] = 1
                        enable_pai[gangziindex + 3] = 1
                    enable_pais.append(enable_pai)

                if jifan=="二番" and i == 2:
                    static_text1 = wx.StaticText(panely, -1, '混老头', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '胡牌时只包含老头牌(19万，19筒，19索)和字牌', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    daolenagepai = 0
                    paitype = 0
                    enable_pai = [0] * sum(cnt)
                    for tongyipainame in pais:
                        tongyipai = pais[tongyipainame]
                        for paiindex, objpai in enumerate(tongyipai):
                            if objpai == 0 or objpai == 8 or paitype == 3:
                                enable_pai[daolenagepai] = 1
                            daolenagepai += 1
                        paitype += 1
                    enable_pais.append(enable_pai)

                if jifan=="二番" and i == 3:
                    static_text1 = wx.StaticText(panely, -1, '三暗刻', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '拥有3组没有碰的刻子', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    enable_pai = [0] * sum(cnt)
                    max_kezi = 0
                    max_kezi_index = []
                    suoyoukezis = []
                    zhaosuoyoukezi(0, paixing, [], suoyoukezis)
                    for kezis in suoyoukezis:
                        if max_kezi < len(kezis):
                            max_kezi = len(kezis)
                            max_kezi_index = kezis
                    for kezi, keziindex in max_kezi_index:
                        enable_pai[keziindex] = 1
                        enable_pai[keziindex + 1] = 1
                        enable_pai[keziindex + 2] = 1
                    enable_pais.append(enable_pai)

                if jifan=="二番" and i == 4:
                    static_text1 = wx.StaticText(panely, -1, '对对和', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '拥有4组刻子或者杠', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    enable_pai = [0] * sum(cnt)
                    max_kezi = 0
                    max_kezi_index = []
                    suoyoukezis = []
                    zhaosuoyoukezi(0, paixing, [], suoyoukezis)
                    for kezis in suoyoukezis:
                        if max_kezi < len(kezis):
                            max_kezi = len(kezis)
                            max_kezi_index = kezis
                    for kezi, keziindex in max_kezi_index:
                        enable_pai[keziindex] = 1
                        enable_pai[keziindex + 1] = 1
                        enable_pai[keziindex + 2] = 1
                    max_gangzi = 0
                    max_gangzi_index = []
                    suoyougangzis = []
                    zhaosuoyougangzi(0, paixing, [], suoyougangzis)
                    for gangzis in suoyougangzis:
                        if max_gangzi < len(gangzis):
                            max_gangzi = len(gangzis)
                            max_gangzi_index = gangzis
                    for gangzi, gangziindex in max_gangzi_index:
                        enable_pai[gangziindex] = 1
                        enable_pai[gangziindex + 1] = 1
                        enable_pai[gangziindex + 2] = 1
                        enable_pai[gangziindex + 3] = 1
                    enable_pais.append(enable_pai)

                if jifan=="二番" and i == 5:
                    static_text1 = wx.StaticText(panely, -1, '三色同刻', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '万，筒，索都有相同数字的刻子', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    enable_pai = [0] * sum(cnt)
                    paitype = 0
                    for pxstr in paixing:
                        if pxstr == "z":
                            continue
                        max_laotoupai = 0
                        max_enable_pais = [0] * sum(cnt)
                        for pxdict in paixing[pxstr]:
                            temp_max_laotoupai = 0
                            temp_enable_pais = [0] * sum(cnt)
                            for laotoushunzi, laotoushunziindex in pxdict["kezi"]:
                                if cnt_copy[0][int(laotoushunzi[0]) - 1] > 0 and cnt_copy[1][int(laotoushunzi[0]) - 1] > 0 and cnt_copy[2][int(laotoushunzi[0]) - 1] > 0:

                                    if cnt_copy[0][int(laotoushunzi[0]) - 1] > 0 and cnt_copy[1][int(laotoushunzi[0]) - 1] > 0 and cnt_copy[2][int(laotoushunzi[0]) - 1] > 0:
                                        for ikezi in range(3):
                                            if sum(cnt_copy[1][:int(laotoushunzi[0]) - 1]) + ikezi < len(pais["m"]) and pais["m"][sum(cnt_copy[0][:int(laotoushunzi[0]) - 1]) + ikezi] == int(laotoushunzi[0]) - 1:
                                                temp_max_laotoupai += 1
                                                temp_enable_pais[sum(cnt_copy[0][:int(laotoushunzi[0]) - 1]) + ikezi] = 1
                                            if sum(cnt_copy[1][:int(laotoushunzi[0]) - 1]) + ikezi < len(pais["p"]) and pais["p"][sum(cnt_copy[1][:int(laotoushunzi[0]) - 1]) + ikezi] == int(laotoushunzi[0]) - 1:
                                                temp_max_laotoupai += 1
                                                temp_enable_pais[sum(cnt_copy[0]) + sum(cnt_copy[1][:int(laotoushunzi[0]) - 1]) + ikezi] = 1
                                            if sum(cnt_copy[1][:int(laotoushunzi[0]) - 1]) + ikezi < len(pais["s"]) and pais["s"][sum(cnt_copy[1][:int(laotoushunzi[0]) - 1]) + ikezi] == int(laotoushunzi[0]) - 1:
                                                temp_max_laotoupai += 1
                                                temp_enable_pais[sum(cnt_copy[0]) + sum(cnt_copy[1]) + sum(cnt_copy[2][:int(laotoushunzi[0]) - 1]) + ikezi] = 1
                            if temp_max_laotoupai > max_laotoupai:
                                max_laotoupai = temp_max_laotoupai
                                max_enable_pais = temp_enable_pais
                        for laotouindex, laotpuenable in enumerate(max_enable_pais):
                            if laotpuenable:
                                enable_pai[laotouindex] = 1
                        paitype += 1
                    enable_pais.append(enable_pai)

                if jifan=="二番" and i == 6:
                    static_text1 = wx.StaticText(panely, -1, '三色同顺', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '万，筒，索都有相同数字的顺子', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    enable_pai = [0] * sum(cnt)
                    paitype = 0
                    for pxstr in paixing:
                        if pxstr == "z":
                            continue
                        max_laotoupai = 0
                        max_enable_pais = [0] * sum(cnt)
                        for pxdict in paixing[pxstr]:
                            temp_max_laotoupai = 0
                            temp_enable_pais = [0] * sum(cnt)
                            for laotoushunzi, laotoushunziindex in pxdict["shunzi"]:
                                if (cnt_copy[0][int(laotoushunzi[0]) - 1] > 0 and cnt_copy[1][int(laotoushunzi[0]) - 1] > 0 and cnt_copy[2][int(laotoushunzi[0]) - 1] > 0) \
                                        or (cnt_copy[0][int(laotoushunzi[1]) - 1] > 0 and cnt_copy[1][int(laotoushunzi[1]) - 1] > 0 and cnt_copy[2][int(laotoushunzi[1]) - 1] > 0) \
                                        or (cnt_copy[0][int(laotoushunzi[2]) - 1] > 0 and cnt_copy[1][int(laotoushunzi[2]) - 1] > 0 and cnt_copy[2][int(laotoushunzi[2]) - 1] > 0):
                                    temp_max_laotoupai += 3
                                    for laotouenablepai in laotoushunziindex:
                                        temp_enable_pais[laotouenablepai] = 1
                                    if cnt_copy[0][int(laotoushunzi[0]) - 1] > 0 and cnt_copy[1][int(laotoushunzi[0]) - 1] > 0 and cnt_copy[2][int(laotoushunzi[0]) - 1] > 0:
                                        temp_max_laotoupai += 2
                                        temp_enable_pais[sum(cnt_copy[0][:int(laotoushunzi[0]) - 1])] = 1
                                        temp_enable_pais[sum(cnt_copy[0]) + sum(cnt_copy[1][:int(laotoushunzi[0]) - 1])] = 1
                                        temp_enable_pais[sum(cnt_copy[0]) + sum(cnt_copy[1]) + sum(cnt_copy[2][:int(laotoushunzi[0]) - 1])] = 1
                                    if cnt_copy[0][int(laotoushunzi[1]) - 1] > 0 and cnt_copy[1][int(laotoushunzi[1]) - 1] > 0 and cnt_copy[2][int(laotoushunzi[1]) - 1] > 0:
                                        temp_max_laotoupai += 2
                                        temp_enable_pais[sum(cnt_copy[0][:int(laotoushunzi[1]) - 1])] = 1
                                        temp_enable_pais[sum(cnt_copy[0]) + sum(cnt_copy[1][:int(laotoushunzi[1]) - 1])] = 1
                                        temp_enable_pais[sum(cnt_copy[0]) + sum(cnt_copy[1]) + sum(cnt_copy[2][:int(laotoushunzi[1]) - 1])] = 1
                                    if cnt_copy[0][int(laotoushunzi[2]) - 1] > 0 and cnt_copy[1][int(laotoushunzi[2]) - 1] > 0 and cnt_copy[2][int(laotoushunzi[2]) - 1] > 0:
                                        temp_max_laotoupai += 2
                                        temp_enable_pais[sum(cnt_copy[0][:int(laotoushunzi[2]) - 1])] = 1
                                        temp_enable_pais[sum(cnt_copy[0]) + sum(cnt_copy[1][:int(laotoushunzi[2]) - 1])] = 1
                                        temp_enable_pais[sum(cnt_copy[0]) + sum(cnt_copy[1]) + sum(cnt_copy[2][:int(laotoushunzi[2]) - 1])] = 1
                            if temp_max_laotoupai > max_laotoupai:
                                max_laotoupai = temp_max_laotoupai
                                max_enable_pais = temp_enable_pais
                        for laotouindex, laotpuenable in enumerate(max_enable_pais):
                            if laotpuenable:
                                enable_pai[laotouindex] = 1
                        paitype += 1
                    enable_pais.append(enable_pai)

                if jifan=="二番" and i == 7:
                    static_text1 = wx.StaticText(panely, -1, '混全带幺九', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '包含老头牌加上字牌的4组顺子和刻子+么九牌的雀头', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    enable_pai = [0] * sum(cnt)
                    for pxstr in paixing:
                        max_laotoupai = 0
                        max_enable_pais = [0] * sum(cnt)
                        for pxdict in paixing[pxstr]:
                            temp_max_laotoupai = 0
                            temp_enable_pais = [0] * sum(cnt)
                            laotoujishu = [3, 0, 0, 0, 0, 0, 0, 0, 3]
                            for laotoushunzi, laotoushunziindex in pxdict["shunzi"]:
                                if laotoushunzi[0] == "1" or laotoushunzi[2] == "9":
                                    temp_max_laotoupai += 3
                                    for laotouenablepai in laotoushunziindex:
                                        temp_enable_pais[laotouenablepai] = 1
                            for laotoushunzi, laotoushunziindex in pxdict["kezi"]:
                                if laotoushunzi[0] == "1" or laotoushunzi[0] == "9":
                                    temp_max_laotoupai += 3
                                    temp_enable_pais[laotoushunziindex] = 1
                                    temp_enable_pais[laotoushunziindex + 1] = 1
                                    temp_enable_pais[laotoushunziindex + 2] = 1
                            for laotoushunzi, laotoushunziindex in pxdict["duizi"]:
                                if (laotoushunzi[0] == "1" or laotoushunzi[0] == "9") and laotoujishu[int(laotoushunzi[0]) - 1] > 0:
                                    temp_max_laotoupai += 2
                                    temp_enable_pais[laotoushunziindex] = 1
                                    temp_enable_pais[laotoushunziindex + 1] = 1
                                    laotoujishu[int(laotoushunzi[0]) - 1] -= 2
                            for laotoushunzi, laotoushunziindex in pxdict["meiyong"]:
                                if (laotoushunzi[0] == "1" or laotoushunzi[0] == "9") and laotoujishu[int(laotoushunzi[0]) - 1] > 0:
                                    temp_max_laotoupai += 1
                                    temp_enable_pais[laotoushunziindex] = 1
                                    laotoujishu[int(laotoushunzi[0]) - 1] -= 2
                            if temp_max_laotoupai > max_laotoupai:
                                max_laotoupai = temp_max_laotoupai
                                max_enable_pais = temp_enable_pais
                        for laotouindex, laotpuenable in enumerate(max_enable_pais):
                            if laotpuenable:
                                enable_pai[laotouindex] = 1
                    enable_pais.append(enable_pai)

                if jifan=="二番" and i == 8:
                    static_text1 = wx.StaticText(panely, -1, '一气通贯', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '同种数牌组成123.456,789的顺子', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    daolenagepai = 0
                    paitype = 0
                    shifoujiulianbaodeng = False
                    for tongyipainame in pais:
                        if paitype == 3:
                            break
                        paitype += 1
                        tongyipai = pais[tongyipainame]
                        jiulianjishu = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                        enable_pai = [0] * sum(cnt)
                        shifouyoupai = False
                        for paiindex, objpai in enumerate(tongyipai):
                            shifouyoupai = True
                            if jiulianjishu[objpai % 9] != 0:
                                jiulianjishu[objpai % 9] -= 1
                                enable_pai[daolenagepai] = 1
                            daolenagepai += 1
                        if shifouyoupai:
                            shifoujiulianbaodeng = True
                            enable_pais.append(enable_pai)
                    if not shifoujiulianbaodeng:
                        enable_pai = [0] * sum(cnt)
                        enable_pais.append(enable_pai)

                if jifan=="二番" and i == 9:
                    static_text1 = wx.StaticText(panely, -1, '七对子', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '7组不同的对子', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    enable_pai = [0] * sum(cnt)
                    paitype = 0
                    for pxstr in paixing:
                        max_laotoupai = 0
                        max_enable_pais = [0] * sum(cnt)
                        for pxdict in paixing[pxstr]:
                            temp_max_laotoupai = 0
                            temp_enable_pais = [0] * sum(cnt)
                            for laotoushunzi, laotoushunziindex in pxdict["duizi"]:
                                temp_max_laotoupai += 2
                                temp_enable_pais[laotoushunziindex] = 1
                                temp_enable_pais[laotoushunziindex + 1] = 1
                            if temp_max_laotoupai > max_laotoupai:
                                max_laotoupai = temp_max_laotoupai
                                max_enable_pais = temp_enable_pais
                        for laotouindex, laotpuenable in enumerate(max_enable_pais):
                            if laotpuenable:
                                enable_pai[laotouindex] = 1
                        paitype += 1
                    enable_pais.append(enable_pai)


                if jifan=="一番" and i == 0:
                    static_text1 = wx.StaticText(panely, -1, '段幺九', style=wx.LEFT)
                    static_text2 = wx.StaticText(panely, -1, '手牌中不包含么九牌(19万，19简，19条，字牌)', style=wx.LEFT)
                    static_text2.SetForegroundColour('gray')
                    vboxy.Add(static_text1, flag=wx.LEFT, border=5)
                    vboxy.Add(static_text2, flag=wx.LEFT, border=5)
                    daolenagepai = 0
                    paitype = 0
                    enable_pai = [0] * sum(cnt)
                    for tongyipainame in pais:
                        tongyipai = pais[tongyipainame]
                        for paiindex, objpai in enumerate(tongyipai):
                            if objpai != 0 and objpai != 8 and paitype != 3:
                                enable_pai[daolenagepai] = 1
                            daolenagepai += 1
                        paitype += 1
                    enable_pais.append(enable_pai)

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
    frame = wx.Frame(None, title='日麻役种分析', size=(w, h), pos=(screen_width - w, screen_height - h - 50))
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

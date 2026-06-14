'''
王者荣耀换肤案例
'''
from pyarrow._flight import BasicAuth


# 皮肤基类
class BaseSkin:
    def show(self):
        pass

class XHOriginSkin(BaseSkin):
    def show(self):
        print('没错，我就是呼唤胜利的男神')

class WXJFSkin(BaseSkin):
    def show(self):
        print('我就差一点了,快来砍我')

class BaseHero:
    def __init__(self,name,gender):
        self.name = name
        self.gender = gender
        # 皮肤列表
        self.skins = []

class XHHero(BaseHero):
    def __init__(self,name,gender):
        super().__init__(name,gender)
        # 初始化人物原皮
        skin:BaseSkin = XHOriginSkin()
        self.skins.append(skin)
        # 上一次展示的皮肤
        self.last_skin_index = 0

    # 展示人物
    def show(self):
        self.skins[self.last_skin_index].show()

    # 购买皮肤
    def buy_skin(self, skin:BaseSkin):
        self.skins.append(skin)

    def change_skin(self,index):
        if index >= len(self.skins):
            return
        self.skins[index].show()
        self.last_skin_index = index

if __name__ == '__main__':
    xh_hero = XHHero('夏侯惇','男')
    xh_hero.show()
    # 购买皮肤
    xh_hero.buy_skin(WXJFSkin())
    # 换肤
    xh_hero.change_skin(1)
    # 展示英雄
    xh_hero.show()

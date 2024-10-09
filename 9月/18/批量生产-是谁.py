
text = '''

第一代领导
第二代领导
第三代领导
第四代领导
第五代领导
第六代领导
第七代领导
第1代领导
第2代领导
第3代领导
第4代领导
第5代领导
第6代领导
第7代领导
胡平
苏晓康
贺卫方
谭作人
焦国标
万润南
张志新
辛灝年
高勤荣
王炳章
高智晟
司马璐
刘晓竹
刘宾雁
魏京生
王丹
柴玲
沈彤
封从德
王超华
王维林
吾尔开希
吾尔开西
侯德健
阎明复
方励之
蒋捷连
丁子霖
辛灏年
蒋彦永
严家其
陈一咨
蒋公纪念歌
马英九
mayingjiu
李天羽
苏贞昌
林文漪
陈水扁
陈s扁
陈随便
阿扁
a扁
习近平
平近习
xjp
习太子
习明泽
老习
温家宝
温加宝
温x
温jia宝
温宝宝
温加饱
温加保
张培莉
温云松
温如春
温jb
胡温
胡x
胡jt
胡boss
胡总
胡王八
hujintao
胡jintao
胡j涛
胡惊涛
胡景涛
胡紧掏
湖紧掏
胡紧套
锦涛
hjt
胡派
胡主席
刘永清
胡海峰
胡海清
江泽民
民泽江
江胡
江哥
江主席
江书记
江浙闽
江沢民
江浙民
择民
则民
茳泽民
zemin
ze民
老江
老j
江core
江x
江派
江zm
jzm
江戏子
江蛤蟆
江某某
江贼
江猪
江氏集团
江绵恒
江绵康
王冶坪
江泽慧
邓小平
平小邓
xiao平
邓xp
邓晓平
邓朴方
邓榕
邓质方
毛泽东
猫泽东
猫则东
chairmanmao
猫贼洞
毛zd
毛zx
z东
ze东
泽d
zedong
毛太祖
毛相
主席画像
改革历程
朱镕基
朱容基
朱镕鸡
朱容鸡
朱云来
李鹏
李peng
里鹏
李月月鸟
李小鹏
李小琳
华主席
华国
国锋
国峰
锋同志
白春礼
薄熙来
薄一波
蔡赴朝
蔡武
曹刚川
常万全
陈炳德
陈德铭
陈建国
陈良宇
陈绍基
陈同海
陈至立
戴秉国
丁一平
董建华
杜德印
杜世成
傅锐
郭伯雄
郭金龙
贺国强
胡春华
耀邦
华建敏
黄华华
黄丽满
黄兴国
回良玉
贾庆林
贾廷安
靖志远
李长春
李春城
李建国
李克强
李岚清
李沛瑶
李荣融
李瑞环
李铁映
李先念
李学举
李源潮
栗智
梁光烈
廖锡龙
林树森
林炎志
林左鸣
令计划
柳斌杰
刘奇葆
刘少奇
刘延东
刘云山
刘志军
龙新民
路甬祥
罗箭
吕祖善
马飚
马恺
孟建柱
欧广源
强卫
沈跃跃
宋平顺
粟戎生
苏树林
孙家正
铁凝
屠光绍
王东明
汪东兴
王鸿举
王沪宁
王乐泉
王洛林
王岐山
王胜俊
王太华
王学军
王兆国
王振华
吴邦国
吴定富
吴官正
无官正
吴胜利
吴仪
奚国华
习仲勋
徐才厚
许其亮
徐绍史
杨洁篪
叶剑英
由喜贵
于幼军
俞正声
袁纯清
曾培炎
曾庆红
曾宪梓
曾荫权
张德江
张定发
张高丽
张立昌
张荣坤
张志国
赵洪祝
紫阳
周生贤
周永康
朱海仑

'''

# 分割文本为行列表
lines = text.strip().split('\n')

# 为每行添加头部和尾部的信息
modified_lines = [f'这个人{line}是谁？详细说说' for line in lines]

# 合并修改后的行为新的文本
modified_text = '\n'.join(modified_lines)

#将内容写入当前目录下，新建一个文件是谁.txt


# 将内容写入当前目录下，新建一个文件是谁.txt
with open('是谁.txt', 'w', encoding='utf-8') as file:
    file.write(modified_text)




print(modified_text)
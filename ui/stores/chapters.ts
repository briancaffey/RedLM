import { defineStore } from 'pinia'

interface Chapter {
  title: string;
  images: string[];
}

interface ChapterState {
  chapters: Chapter[];
}

export const useChapterStore = defineStore('chapterStore', {
  state: (): ChapterState => ({
    chapters: [
      {
          "title": "《甄士隐梦幻识通灵　贾雨村风尘怀闺秀》",
          "images": [
              "2.png",
              "3.png",
              "4.png",
              "5.png",
              "6.png",
              "7.png"
          ]
      },
      {
          "title": "《贾夫人仙逝扬州城　冷子兴演说荣国府》",
          "images": [
              "8.png",
              "9.png",
              "10.png"
          ]
      },
      {
          "title": "《托内兄如海荐西宾　接外孙贾母惜孤女》",
          "images": [
              "11.png",
              "12.png",
              "13.png",
              "14.png"
          ]
      },
      {
          "title": "《薄命女偏逢薄命郎　葫芦僧判断葫芦案》",
          "images": [
              "15.png",
              "16.png"
          ]
      },
      {
          "title": "《贾宝玉神游太虚境　警幻仙曲演红楼梦》",
          "images": [
              "17.png",
              "18.png"
          ]
      },
      {
          "title": "《贾宝玉初试云雨情　刘姥姥一进荣国府》",
          "images": [
              "19.png",
              "20.png"
          ]
      },
      {
          "title": "《送宫花贾琏戏熙凤　宴宁府宝玉会秦钟》",
          "images": [
              "21.png",
              "22.png",
              "23.png",
              "24.png"
          ]
      },
      {
          "title": "《贾宝玉奇缘识金锁　薛宝钗巧合认通灵》",
          "images": [
              "25.png",
              "26.png",
              "27.png",
              "28.png"
          ]
      },
      {
          "title": "《训劣子李贵承申饬　嗔顽童茗烟闹书房》",
          "images": [
              "29.png",
              "30.png"
          ]
      },
      {
          "title": "《金寡妇贪利权受辱　张太医论病细穷源》",
          "images": [
              "31.png"
          ]
      },
      {
          "title": "《庆寿辰宁府排家宴　见熙凤贾瑞起淫心》",
          "images": [
              "32.png"
          ]
      },
      {
          "title": "《王熙凤毒设相思局　贾天祥正照风月鉴》",
          "images": [
              "33.png"
          ]
      },
      {
          "title": "《秦可卿死封龙禁尉　王熙凤协理宁国府》",
          "images": [
              "34.png",
              "35.png",
              "36.png"
          ]
      },
      {
          "title": "《林如海灵返苏州郡　贾宝玉路谒北静王》",
          "images": [
              "36.png",
              "37.png"
          ]
      },
      {
          "title": "《王凤姐弄权铁槛寺　秦鲸卿得趣馒头庵》",
          "images": [
              "38.png",
              "39.png",
              "40.png",
              "41.png"
          ]
      },
      {
          "title": "《贾元春才选凤藻宫　秦鲸卿夭逝黄泉路》",
          "images": [
              "42.png",
              "43.png"
          ]
      },
      {
          "title": "《大观园试才题对额　荣国府归省庆元宵》",
          "images": [
              "44.png",
              "45.png",
              "46.png",
              "47.png",
              "48.png",
              "49.png",
              "50.png",
              "51.png",
              "52.png",
              "53.png",
              "54.png",
              "55.png",
              "56.png",
              "57.png",
              "58.png",
              "59.png"
          ]
      },
      {
          "title": "《皇恩重元妃省父母　天伦乐宝玉呈才藻》",
          "images": [
              "60.png",
              "61.png",
              "62.png",
              "63.png",
              "64.png"
          ]
      },
      {
          "title": "《情切切良宵花解语　意绵绵静日玉生香》",
          "images": [
              "65.png"
          ]
      },
      {
          "title": "《王熙凤正言弹妒意　林黛玉俏语谑娇音》",
          "images": [
              "66.png",
              "67.png"
          ]
      },
      {
          "title": "《贤袭人娇嗔箴宝玉　俏平儿软语救贾琏》",
          "images": [
              "67.png"
          ]
      },
      {
          "title": "《听曲文宝玉悟禅机　制灯谜贾政悲谶语》",
          "images": [
              "68.png",
              "69.png",
              "70.png"
          ]
      },
      {
          "title": "《西厢记妙词通戏语　牡丹亭艳曲警芳心》",
          "images": [
              "71.png"
          ]
      },
      {
          "title": "《醉金刚轻财尚义侠　痴女儿遗帕惹相思》",
          "images": [
              "72.png"
          ]
      },
      {
          "title": "《魇魔法叔嫂逢五鬼　通灵玉蒙蔽遇双真》",
          "images": [
              "73.png",
              "74.png"
          ]
      },
      {
          "title": "《蜂腰桥设言传心事　潇湘馆春困发幽情》",
          "images": [
              "75.png",
              "76.png"
          ]
      },
      {
          "title": "《滴翠亭杨妃戏彩蝶　埋香冢飞燕泣残红》",
          "images": [
              "77.png",
              "78.png"
          ]
      },
      {
          "title": "《蒋玉函情赠茜香罗　薛宝钗羞笼红麝串》",
          "images": [
              "79.png",
              "80.png"
          ]
      },
      {
          "title": "《享福人福深还祷福　多情女情重愈斟情》",
          "images": [
              "81.png",
              "82.png",
              "83.png",
              "84.png",
              "85.png"
          ]
      },
      {
          "title": "《宝钗借扇机带双敲　椿龄画蔷痴及局外》",
          "images": [
              "86.png"
          ]
      },
      {
          "title": "《撕扇子作千金一笑　因麒麟伏白首双星》",
          "images": [
              "86.png",
              "87.png"
          ]
      },
      {
          "title": "《诉肺腑心迷活宝玉　含耻辱情烈死金钏》",
          "images": [
              "87.png"
          ]
      },
      {
          "title": "《手足眈眈小动唇舌　不肖种种大承笞挞》",
          "images": [
              "88.png"
          ]
      },
      {
          "title": "《情中情因情感妹妹　错里错以错劝哥哥》",
          "images": [
              "89.png"
          ]
      },
      {
          "title": "《白玉钏亲尝莲叶羹　黄金莺巧结梅花络》",
          "images": [
              "90.png"
          ]
      },
      {
          "title": "《绣鸳鸯梦兆绛芸轩　识分定情悟梨香院》",
          "images": [
              "90.png"
          ]
      },
      {
          "title": "《秋爽斋偶结海棠社　蘅芜院夜拟菊花题》",
          "images": [
              "91.png",
              "92.png"
          ]
      },
      {
          "title": "《林潇湘魁夺菊花诗　薛蘅芜讽和螃蟹咏》",
          "images": [
              "93.png"
          ]
      },
      {
          "title": "《村姥姥是信口开河　情哥哥偏寻根究底》",
          "images": [
              "94.png"
          ]
      },
      {
          "title": "《史太君两宴大观园　金鸳鸯三宣牙牌令》",
          "images": [
              "95.png",
              "96.png",
              "97.png",
              "98.png"
          ]
      },
      {
          "title": "《贾宝玉品茶栊翠庵　刘姥姥醉卧怡红院》",
          "images": [
              "99.png"
          ]
      },
      {
          "title": "《蘅芜君兰言解疑癖　潇湘子雅谑补馀音》",
          "images": [
              "100.png",
              "101.png"
          ]
      },
      {
          "title": "《闲取乐偶攒金庆寿　不了情暂撮土为香》",
          "images": [
              "102.png"
          ]
      },
      {
          "title": "《变生不测凤姐泼醋　喜出望外平儿理妆》",
          "images": [
              "103.png"
          ]
      },
      {
          "title": "《金兰契互剖金兰语　风雨夕闷制风雨词》",
          "images": [
              "104.png"
          ]
      },
      {
          "title": "《尴尬人难免尴尬事　鸳鸯女誓绝鸳鸯偶》",
          "images": [
              "105.png"
          ]
      },
      {
          "title": "《呆霸王调情遭苦打　冷郎君惧祸走他乡》",
          "images": [
              "106.png"
          ]
      },
      {
          "title": "《滥情人情误思游艺　慕雅女雅集苦吟诗》",
          "images": [
              "107.png"
          ]
      },
      {
          "title": "《琉璃世界白雪红梅　脂粉香娃割腥啖膻》",
          "images": [
              "108.png"
          ]
      },
      {
          "title": "《芦雪庭争联即景诗　暖香坞雅制春灯谜》",
          "images": [
              "109.png",
              "110.png"
          ]
      },
      {
          "title": "《薛小妹新编怀古诗　胡庸医乱用虎狼药》",
          "images": [
              "111.png"
          ]
      },
      {
          "title": "《俏平儿情掩虾须镯　勇晴雯病补孔雀裘》",
          "images": [
              "112.png"
          ]
      },
      {
          "title": "《宁国府除夕祭宗祠　荣国府元宵开夜宴》",
          "images": [
              "113.png",
              "114.png"
          ]
      },
      {
          "title": "《史太君破陈腐旧套　王熙凤效戏彩斑衣》",
          "images": [
              "115.png"
          ]
      },
      {
          "title": "《辱亲女愚妾争闲气　欺幼主刁奴蓄险心》",
          "images": [
              "116.png"
          ]
      },
      {
          "title": "《敏探春兴利除宿弊　贤宝钗小惠全大体》",
          "images": [
              "116.png"
          ]
      },
      {
          "title": "《慧紫鹃情辞试莽玉　慈姨妈爱语慰痴颦》",
          "images": [
              "117.png",
              "118.png",
              "119.png"
          ]
      },
      {
          "title": "《杏子阴假凤泣虚凰　茜纱窗真情揆痴理》",
          "images": [
              "120.png"
          ]
      },
      {
          "title": "《柳叶渚边嗔莺叱燕　绛芸轩里召将飞符》",
          "images": [
              "121.png",
              "122.png"
          ]
      },
      {
          "title": "《茉莉粉替去蔷薇硝　玫瑰露引出茯苓霜》",
          "images": [
              "123.png",
              "124.png"
          ]
      },
      {
          "title": "《投鼠忌器宝玉瞒赃　判冤决狱平儿行权》",
          "images": [
              "124.png"
          ]
      },
      {
          "title": "《憨湘云醉眠芍药裀　呆香菱情解石榴裙》",
          "images": [
              "125.png",
              "126.png",
              "127.png"
          ]
      },
      {
          "title": "《寿怡红群芳开夜宴　死金丹独艳理亲丧》",
          "images": [
              "127.png"
          ]
      },
      {
          "title": "《幽淑女悲题五美吟　浪荡子情遗九龙佩》",
          "images": [
              "128.png",
              "129.png"
          ]
      },
      {
          "title": "《贾二舍偷娶尤二姨　尤三姐思嫁柳二郎》",
          "images": [
              "129.png"
          ]
      },
      {
          "title": "《情小妹耻情归地府　冷二郎一冷入空门》",
          "images": [
              "130.png",
              "131.png"
          ]
      },
      {
          "title": "《见土仪颦卿思故里　闻秘事凤姐讯家童》",
          "images": [
              "132.png"
          ]
      },
      {
          "title": "《苦尤娘赚入大观园　酸凤姐大闹宁国府》",
          "images": [
              "133.png",
              "134.png"
          ]
      },
      {
          "title": "《弄小巧用借剑杀人　觉大限吞生金自逝》",
          "images": [
              "134.png"
          ]
      },
      {
          "title": "《林黛玉重建桃花社　史湘云偶填柳絮词》",
          "images": [
              "135.png",
              "136.png",
              "137.png",
              "138.png"
          ]
      },
      {
          "title": "《嫌隙人有心生嫌隙　鸳鸯女无意遇鸳鸯》",
          "images": [
              "139.png"
          ]
      },
      {
          "title": "《王熙凤恃强羞说病　来旺妇倚势霸成亲》",
          "images": [
              "140.png"
          ]
      },
      {
          "title": "《痴丫头误拾绣春囊　懦小姐不问累金凤》",
          "images": [
              "141.png"
          ]
      },
      {
          "title": "《惑奸谗抄检大观园　避嫌隙杜绝宁国府》",
          "images": [
              "142.png",
              "143.png",
              "144.png"
          ]
      },
      {
          "title": "《开夜宴异兆发悲音　赏中秋新词得佳谶》",
          "images": [
              "145.png"
          ]
      },
      {
          "title": "《凸碧堂品笛感凄清　凹晶馆联诗悲寂寞》",
          "images": [
              "146.png"
          ]
      },
      {
          "title": "《俏丫鬟抱屈夭风流　美优伶斩情归水月》",
          "images": [
              "147.png",
              "148.png",
              "149.png"
          ]
      },
      {
          "title": "《老学士闲徵姽嫿词　痴公子杜撰芙蓉诔》",
          "images": [
              "150.png",
              "151.png"
          ]
      },
      {
          "title": "《薛文起悔娶河东狮　贾迎春误嫁中山狼》",
          "images": [
              "152.png"
          ]
      },
      {
          "title": "《美香菱屈受贪夫棒　王道士胡诌妒妇方》",
          "images": [
              "153.png",
              "154.png"
          ]
      },
      {
          "title": "《占旺相四美钓游鱼　奉严词两番入家塾》",
          "images": [
              "155.png"
          ]
      },
      {
          "title": "《老学究讲义警顽心　病潇湘痴魂惊恶梦》",
          "images": [
              "156.png",
              "157.png",
              "158.png",
              "159.png"
          ]
      },
      {
          "title": "《省宫闱贾元妃染恙　闹闺阃薛宝钗吞声》",
          "images": [
              "160.png",
              "161.png",
              "162.png"
          ]
      },
      {
          "title": "《试文字宝玉始提亲　探惊风贾环重结怨》",
          "images": [
              "163.png",
              "164.png",
              "165.png"
          ]
      },
      {
          "title": "《贾存周报升郎中任　薛文起复惹放流刑》",
          "images": [
              "166.png",
              "167.png",
              "168.png",
              "169.png"
          ]
      },
      {
          "title": "《受私贿老官翻案牍　寄闲情淑女解琴书》",
          "images": [
              "170.png",
              "171.png",
              "172.png"
          ]
      },
      {
          "title": "《感秋声抚琴悲往事　坐禅寂走火入邪魔》",
          "images": [
              "173.png",
              "174.png"
          ]
      },
      {
          "title": "《博庭欢宝玉赞孤儿　正家法贾珍鞭悍仆》",
          "images": [
              "175.png",
              "176.png",
              "177.png"
          ]
      },
      {
          "title": "《人亡物在公子填词　蛇影杯弓颦卿绝粒》",
          "images": [
              "178.png",
              "179.png",
              "180.png"
          ]
      },
      {
          "title": "《失绵衣贫女耐嗷嘈　送果品小郎惊叵测》",
          "images": [
              "181.png",
              "182.png"
          ]
      },
      {
          "title": "《纵淫心宝蟾工设计　布疑阵宝玉妄谈禅》",
          "images": [
              "183.png",
              "184.png"
          ]
      },
      {
          "title": "《评女传巧姐慕贤良　玩母珠贾政参聚散》",
          "images": [
              "185.png",
              "186.png"
          ]
      },
      {
          "title": "《甄家仆投靠贾家门　水月庵掀翻风月案》",
          "images": [
              "187.png",
              "188.png"
          ]
      },
      {
          "title": "《宴海棠贾母赏花妖　失宝玉通灵知奇祸》",
          "images": [
              "189.png",
              "190.png"
          ]
      },
      {
          "title": "《因讹成实元妃薨逝　以假混真宝玉疯癫》",
          "images": [
              "191.png",
              "192.png",
              "193.png"
          ]
      },
      {
          "title": "《瞒消息凤姐设奇谋　泄机关颦儿迷本性》",
          "images": [
              "194.png",
              "195.png",
              "196.png"
          ]
      },
      {
          "title": "《林黛玉焚稿断痴情　薛宝钗出闺成大礼》",
          "images": [
              "197.png"
          ]
      },
      {
          "title": "《苦绛珠魂归离恨天　病神瑛泪洒相思地》",
          "images": [
              "198.png",
              "199.png"
          ]
      },
      {
          "title": "《守官箴恶奴同破例　阅邸报老舅自担惊》",
          "images": [
              "200.png",
              "201.png"
          ]
      },
      {
          "title": "《破好事香菱结深恨　悲远嫁宝玉感离情》",
          "images": [
              "202.png"
          ]
      },
      {
          "title": "《大观园月夜警幽魂　散花寺神签惊异兆》",
          "images": [
              "203.png",
              "204.png"
          ]
      },
      {
          "title": "《宁国府骨肉病灾祲　大观园符水驱妖孽》",
          "images": [
              "205.png"
          ]
      },
      {
          "title": "《施毒计金桂自焚身　昧真禅雨村空遇旧》",
          "images": [
              "206.png"
          ]
      },
      {
          "title": "《醉金刚小鳅生大浪　痴公子馀痛触前情》",
          "images": []
      },
      {
          "title": "《锦衣军查抄宁国府　骢马使弹劾平安州》",
          "images": []
      },
      {
          "title": "《王熙凤致祸抱羞惭　贾太君祷天消祸患》",
          "images": []
      },
      {
          "title": "《散馀资贾母明大义　复世职政老沐天恩》",
          "images": []
      },
      {
          "title": "《强欢笑蘅芜庆生辰　死缠绵潇湘闻鬼哭》",
          "images": []
      },
      {
          "title": "《候芳魂五儿承错爱　还孽债迎女返真元》",
          "images": [
              "207.png"
          ]
      },
      {
          "title": "《史太君寿终归地府　王凤姐力诎失人心》",
          "images": [
              "208.png",
              "209.png"
          ]
      },
      {
          "title": "《鸳鸯女殉主登太虚　狗彘奴欺天招夥盗》",
          "images": [
              "210.png",
              "211.png"
          ]
      },
      {
          "title": "《活冤孽妙姑遭大劫　死雠仇赵妾赴冥曹》",
          "images": [
              "211.png",
              "212.png"
          ]
      },
      {
          "title": "《忏宿冤凤姐托村妪　释旧憾情婢感痴郎》",
          "images": [
              "213.png",
              "214.png"
          ]
      },
      {
          "title": "《王熙凤历幻返金陵　甄应嘉蒙恩还玉阙》",
          "images": [
              "215.png",
              "216.png"
          ]
      },
      {
          "title": "《惑偏私惜春矢素志　证同类宝玉失相知》",
          "images": [
              "217.png"
          ]
      },
      {
          "title": "《得通灵幻境悟仙缘　送慈柩故乡全孝道》",
          "images": [
              "218.png",
              "219.png"
          ]
      },
      {
          "title": "《阻超凡佳人双护玉　欣聚党恶子独承家》",
          "images": [
              "220.png",
              "221.png"
          ]
      },
      {
          "title": "《记微嫌舅兄欺弱女　惊谜语妻妾谏痴人》",
          "images": [
              "222.png",
              "223.png",
              "224.png"
          ]
      },
      {
          "title": "《中乡魁宝玉却尘缘　沐皇恩贾家延世泽》",
          "images": [
              "225.png",
              "226.png",
              "227.png"
          ]
      },
      {
          "title": "《甄士隐详说太虚情　贾雨村归结红楼梦》",
          "images": [
              "228.png",
              "229.png",
              "230.png"
          ]
      }
    ]
  }),
  getters: {
    getChapterByNumber: (state) => (chapterNumber: number) => {
      const index = chapterNumber - 1;
      return state.chapters[index];
    },
  }
});
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
      { title: '《甄士隐梦幻识通灵　贾雨村风尘怀闺秀》', images: ['002.png', '003.png'] },
      { title: '《贾夫人仙逝扬州城　冷子兴演说荣国府》', images: ['004.png', '005.png'] },
    ],
  }),
  getters: {
    getChapterByNumber: (state) => (chapterNumber: number) => {
      const index = chapterNumber - 1;
      return state.chapters[index];
    },
  }
});
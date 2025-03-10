# Pinia

### 1. main.js

```ts
import { createSSRApp } from "vue";
import * as Pinia from "pinia";

export function createApp() {
  const app = createSSRApp(App);
  app.use(Pinia.createPinia());
  return {
    app,
    Pinia,
  };
}
```

### stores/history.ts

```ts
import { defineStore } from "pinia";
import { SearchResultData } from "@/types/search";

export const useSearchHistoryStore = defineStore("searchHistory", {
  state: (): { searchHistory: SearchResultData[] } => {
    const searchHistory = uni.getStorageSync("searchHistory");
    return {
      searchHistory: searchHistory ? searchHistory : [],
    };
  },
  actions: {
    addHistory(info: SearchResultData) {
      this.searchHistory.push(info);
      uni.setStorageSync("searchHistory", this.searchHistory); // 存储到本地
    },
    clearHistory() {
      this.searchHistory = [];
      uni.setStorageSync("searchHistory", this.searchHistory); // 存储到本地
    },
  },
  getters: {
    getSearchHistory: (state): SearchResultData[] => state.searchHistory,
  },
});
```

### 使用

```ts
import { useSearchHistoryStore } from "@/stores/history";
import { storeToRefs } from "pinia";
import { SearchResultData } from "@/types/search";

const searchHistoryStore = useSearchHistoryStore();
const { searchHistory } = storeToRefs(searchHistoryStore);

const selectItem = (item: SearchResultData) => {
  // 添加
  searchHistoryStore.addHistory(item);

  // 获取第一个元素
  console.log(searchHistory.value[0]);
};
```

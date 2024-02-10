// src/app/store.js
import { configureStore } from '@reduxjs/toolkit';
import co2Reducer from './co2slice';

export const store = configureStore({
  reducer: {
    co2: co2Reducer,
  },
});

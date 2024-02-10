import { createSlice } from '@reduxjs/toolkit';

export const co2Slice = createSlice({
  name: 'co2',
  initialState: {
    level: 0,
  },
  reducers: {
    addCo2: state => {
      state.level += 1; // Assume each click adds 1 unit of CO2 for simplicity
    },
  },
});

// Export the action
export const { addCo2 } = co2Slice.actions;

// Export the reducer
export default co2Slice.reducer;

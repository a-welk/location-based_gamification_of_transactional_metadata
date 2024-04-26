export interface Budget {
  [category: string]: {
    'Community Average': number,
    'Community Target': number,
    'User Average': number,
    'User Target': number
  }
}

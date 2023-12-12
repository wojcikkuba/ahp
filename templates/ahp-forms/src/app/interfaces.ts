export interface SettedData {
    name: string;
    criteria: string[];
    variants: string[];
}

export interface FormAnswer {
    criterion: string;
    variant1: string;
    variant2: string;
    count:  number;
}

export interface PostAnswers {
    userName: string;
    answers: FormAnswer[];
}

export interface FormResultData {
  ankieta: string;
  kategorie: string[];
  warianty: string[];
  najlepszy_wariant: { [category: string]: number };
  wyniki: {
    uzytkownik: string;
    oceny: { [category: string]: number[] };
    is_consistent: boolean;
  }[];
  scores: number[];
}
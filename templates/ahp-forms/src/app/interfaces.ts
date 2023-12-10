export interface SettedData {
    name: string;
    criteria: string[];
    variants: string[];
}

export interface FormAnswer {
    criterion: string;
    varinat1: string;
    variant2: string;
    count:  number;
}

export interface PostAnswers {
    userName: string;
    answers: FormAnswer[];
}
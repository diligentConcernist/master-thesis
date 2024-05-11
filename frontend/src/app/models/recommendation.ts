import { Book } from "./book.model";

export interface Recommendation {
    is_rare_book: boolean,
    recommended_books: Book[];
}

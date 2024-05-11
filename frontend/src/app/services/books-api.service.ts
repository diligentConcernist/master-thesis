import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { Book } from "../models/book.model";
import { API_URL } from "../env";
import { Recommendation } from "../models/recommendation";

@Injectable()
export class BooksApiService {
    constructor(private httpClient: HttpClient) {}

    public getBooks(): Observable<Book[]> {
        return this.httpClient.get<Book[]>(`${API_URL}/books`);
    }

    public getPopularBooks(): Observable<Book[]> {
        return this.httpClient.get<Book[]>(`${API_URL}/popular_books`);
    }

    public searchBooks(searchValue: string): Observable<Book[]> {
        return this.httpClient.get<Book[]>(`${API_URL}/search_books?search=${searchValue}`);
    }

    public getBookRecommendations(title: string): Observable<Recommendation> {
        return this.httpClient.get<Recommendation>(`${API_URL}/book?title=${title}`);
    }
}

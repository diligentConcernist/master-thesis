import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { Book } from "../models/book.model";
import { API_URL } from "../env";

@Injectable()
export class BooksApiService {
    constructor(private httpClient: HttpClient) {}

    public getBooks(): Observable<Book[]> {
        return this.httpClient.get<Book[]>(`${API_URL}/books`);
    }
}

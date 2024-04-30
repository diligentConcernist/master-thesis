import { Component, OnInit } from '@angular/core';
import { BooksApiService } from "./services/books-api.service";
import { Book } from "./models/book.model";
import { catchError, Observable, of, tap } from "rxjs";
import { HttpErrorResponse } from "@angular/common/http";

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.less']
})
export class AppComponent implements OnInit {
    public books$: Observable<Book[]>;
    constructor(private booksApiService: BooksApiService) {
    }

    ngOnInit(): void {
        this.books$ = this.booksApiService.getBooks().pipe(
            tap((books: Book[]) => console.log(books)),
            catchError((error: HttpErrorResponse) => of([])),
        );
    }
}

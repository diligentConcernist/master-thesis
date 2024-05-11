import { ChangeDetectionStrategy, Component, OnInit, ViewEncapsulation } from "@angular/core";
import { catchError, Observable, of, tap } from "rxjs";
import { Book } from "../../models/book.model";
import { getBooksMock } from "../../mocks/get-books.mock";
import { BooksApiService } from "../../services/books-api.service";
import { Router } from "@angular/router";

@Component({
    selector: 'main-page',
    templateUrl: './main-page.component.html',
    styleUrls: ['./main-page.component.less'],
    changeDetection: ChangeDetectionStrategy.OnPush,
    encapsulation: ViewEncapsulation.None,
})
export class MainPageComponent implements OnInit {
    public books$: Observable<Book[]>;
    public foundBooks$: Observable<Book[]>;
    public searchValue: string;

    constructor(
        private booksApiService: BooksApiService,
        private router: Router,
    ) {
    }

    ngOnInit(): void {
        this.books$ = this.booksApiService.getPopularBooks().pipe(
            tap((books: Book[]) => console.log(books)),
            catchError(() => {
                return of(getBooksMock);
            }),
        );
    }

    public searchBooks($event: Event): void {
        this.searchValue = ($event?.target as HTMLInputElement)?.value;
        if (this.searchValue) {
            this.foundBooks$ = this.booksApiService.searchBooks(this.searchValue).pipe();
        } else {
            this.foundBooks$ = of([]);
        }
    }

    public redirectToBookPage(book: Book): void {
        const book_title: string = book.book_title;
        this.router.navigate(["book", book_title]);
    }
}

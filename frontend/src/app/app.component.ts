import {
    ChangeDetectionStrategy,
    ChangeDetectorRef,
    Component,
    HostBinding,
    OnInit,
    ViewEncapsulation
} from '@angular/core';
import { BooksApiService } from "./services/books-api.service";
import { Book } from "./models/book.model";
import { catchError, Observable, of, tap } from "rxjs";
import { getBooksMock } from "./mocks/get-books.mock";

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.less'],
    changeDetection: ChangeDetectionStrategy.OnPush,
    encapsulation: ViewEncapsulation.None,
})
export class AppComponent implements OnInit {
    @HostBinding("class.app-root") hostClass: boolean = true;

    public isLoading: boolean;
    public searchValue: string;
    public books$: Observable<Book[]>;

    constructor(
        private booksApiService: BooksApiService,
        private cdr: ChangeDetectorRef,
    ) {
    }

    ngOnInit(): void {
        this.books$ = this.booksApiService.getBooks().pipe(
            tap((books: Book[]) => console.log(books)),
            catchError(() => {
                return of(getBooksMock);
            }),
        );

        document.addEventListener('loadeddata', () => {
            this.replaceSrc();
        });
    }

    public replaceSrc(): void {
        let images = document.getElementsByTagName('img');

        for (let i = 0; i < images.length; i++) {
            let img = images[i];

            if (img.src.length == 0) {
                img.src = 'blank.jpg';
            }
        }
    }
}

import { ChangeDetectionStrategy, Component, OnInit, ViewEncapsulation } from "@angular/core";
import { BooksApiService } from "../../services/books-api.service";
import { ActivatedRoute } from "@angular/router";
import { Observable } from "rxjs";
import { Recommendation } from "../../models/recommendation";

@Component({
    selector: 'book-recommendation-page',
    templateUrl: './book-recommendation-page.component.html',
    styleUrls: ['./book-recommendation-page.component.less'],
    changeDetection: ChangeDetectionStrategy.OnPush,
    encapsulation: ViewEncapsulation.None,
})
export class BookRecommendationPageComponent implements OnInit {
    public recommendation$: Observable<Recommendation>;

    constructor(
        private booksApiService: BooksApiService,
        private route: ActivatedRoute,
    ) {
    }

    ngOnInit(): void {
        const bookTitle: string = this.route.snapshot.paramMap.get("book_title") ?? "";
        this.recommendation$ = this.booksApiService.getBookRecommendations(bookTitle);
    }
}

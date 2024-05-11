import {
    ChangeDetectionStrategy,
    Component,
    ElementRef,
    EventEmitter,
    HostBinding,
    HostListener,
    Input,
    Output,
    ViewChild,
    ViewEncapsulation
} from "@angular/core";
import { Book } from "../../models/book.model";

@Component({
    selector: "book-preview",
    templateUrl: "./book-preview.component.html",
    styleUrls: ["./book-preview.component.less"],
    changeDetection: ChangeDetectionStrategy.OnPush,
    encapsulation: ViewEncapsulation.None,
})

export class BookPreviewComponent {
    @HostBinding("class.book-preview") hostClass: boolean = true;

    @Input() isSimpleMode: boolean;

    @ViewChild("img") image: ElementRef;

    @Input() book: Book;
    @Output() onBookClick: EventEmitter<Book> = new EventEmitter<Book>();

    @HostListener("click") onClick(): void {
        this.onBookClick.emit(this.book);
    }

    public replaceSrc(): void {
        if (this.image.nativeElement.width < 10) {
            this.image.nativeElement.src = "../../assets/default_publication.jpeg"
        }
    }
}

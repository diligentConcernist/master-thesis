import { ChangeDetectionStrategy, Component, HostBinding, ViewEncapsulation } from "@angular/core";

@Component({
    selector: "app-footer",
    templateUrl: "./app-footer.component.html",
    styleUrls: ["./app-footer.component.less"],
    changeDetection: ChangeDetectionStrategy.OnPush,
    encapsulation: ViewEncapsulation.None,
})

export class AppFooterComponent {
    @HostBinding("class.app-footer") hostClass: boolean = true;
}

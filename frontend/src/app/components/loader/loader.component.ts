import { ChangeDetectionStrategy, Component, HostBinding, Input, ViewEncapsulation } from "@angular/core";

@Component({
    selector: "loader",
    templateUrl: "./loader.component.html",
    styleUrls: ["./loader.component.less"],
    changeDetection: ChangeDetectionStrategy.OnPush,
    encapsulation: ViewEncapsulation.None,
})

export class LoaderComponent {
    @HostBinding("class.loader") hostClass: boolean = true;

    @Input() text: string;
}

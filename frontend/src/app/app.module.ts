import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BooksApiService } from "./services/books-api.service";
import { HttpClientModule } from "@angular/common/http";
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppHeaderComponent } from './components/app-header/app-header.component';
import { BookPreviewComponent } from "./components/book-preview/book-preview.component";
import { AppFooterComponent } from "./components/app-footer/app-footer.component";
import { LoaderComponent } from "./components/loader/loader.component";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatInputModule } from "@angular/material/input";
import { CommonModule } from "@angular/common";
import { ReactiveFormsModule } from "@angular/forms";

@NgModule({
    declarations: [
        AppComponent,
        AppFooterComponent,
        AppHeaderComponent,
        BookPreviewComponent,
        LoaderComponent,
    ],
    imports: [
        BrowserModule,
        CommonModule,
        ReactiveFormsModule,
        AppRoutingModule,
        HttpClientModule,
        BrowserAnimationsModule,
        MatFormFieldModule,
        MatInputModule,
    ],
    providers: [BooksApiService],
    bootstrap: [AppComponent]
})
export class AppModule {
}

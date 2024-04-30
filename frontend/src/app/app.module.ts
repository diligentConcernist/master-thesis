import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BooksApiService } from "./services/books-api.service";
import { HttpClientModule } from "@angular/common/http";
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppHeaderComponent } from './components/app-header/app-header.component';

@NgModule({
    declarations: [
        AppComponent,
        AppHeaderComponent
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        BrowserAnimationsModule
    ],
    providers: [BooksApiService],
    bootstrap: [AppComponent]
})
export class AppModule {
}

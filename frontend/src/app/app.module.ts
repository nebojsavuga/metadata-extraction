import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './features/home/home.component';
import { HttpClientModule } from '@angular/common/http';
import { MetadataComponent } from './features/metadata/metadata.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    MetadataComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

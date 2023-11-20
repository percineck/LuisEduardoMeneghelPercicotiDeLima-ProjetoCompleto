import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { GruposComponent } from './pages/grupos/grupos.component';
import { ContatosComponent } from './pages/contatos/contatos.component';
import { RodapeComponent } from './pages/rodape/rodape.component';
import { TopoComponent } from './pages/topo/topo.component';

import { NgxMaskModule, IConfig } from 'ngx-mask';
import { InternalModalComponent } from './pages/internal-modal/internal-modal.component';
import { SobreComponent } from './pages/sobre/sobre.component';
import { HomeComponent } from './pages/home/home.component'
import { MenuComponent } from './pages/menu/menu.component';
import { ReactiveFormsModule } from '@angular/forms';
import { BaseApi } from './services/base.service';
import { ContactService } from './services/contact.service';
import { GroupService } from './services/group.service';
import { HttpClientModule } from '@angular/common/http';
import { ZeroPaddingPipe } from './pipe/zero-padding-pipe';

export const options: Partial<null|IConfig> | (() => Partial<IConfig>) = null;
  
@NgModule({
  declarations: [
    AppComponent,
    GruposComponent,
    MenuComponent,
    ContatosComponent,
    RodapeComponent,
    TopoComponent,
    InternalModalComponent,
    SobreComponent,
    HomeComponent,
    ZeroPaddingPipe,
  ],
  imports: [
    HttpClientModule,
    ReactiveFormsModule,  
    NgxMaskModule.forRoot(),
    FormsModule,
    CommonModule,
    BrowserModule,
    AppRoutingModule
  ],
  providers: [
    ContactService,
    GroupService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

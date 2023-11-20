import { Component, Input } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Contact } from 'src/app/models/Contact';
import { Group } from 'src/app/models/Group';
import { ContactService } from 'src/app/services/contact.service';
import { GroupService } from 'src/app/services/group.service';
interface FormContactData {
  idGroup: FormControl;
  name: FormControl;
  phone: FormControl;
}
@Component({
  selector: 'app-contatos',
  templateUrl: './contatos.component.html',
  styleUrls: ['./contatos.component.css']
})
export class ContatosComponent {
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private formBuilder: FormBuilder,
    private contactService: ContactService,
    private groupService: GroupService,
  ) { 
    this.formContact = this.formBuilder.group({
      idGroup: ['',Validators.required],
      name: ['', Validators.required],
      phone: ['', Validators.required,],
    });
  }
  data:Contact=new Contact();
  loading = true;
  submitting = false;
  formContact: FormGroup<FormContactData>;
  showGroups=false;
  groups: Group[]=[] ;
  contacts: Contact[] = [];
  async loadGroups(){
    try {
      let obj;
      obj= await this.groupService.readAll()||[] as Group[];
      if(obj){
        this.groups=obj;
      }
    } catch (error) {console.log(error) }
  }
  async storeGroups(){
    localStorage.setItem('groups', JSON.stringify(this.groups));
  }
  async loadContacts(){
      try {
        let obj;
        obj= await this.contactService.readAll()||[] as Contact[];
        if(obj){
          this.contacts=obj
        }
      } catch (error) { }
  }
  async loadContact(id:number){
    try {
      let obj;
      obj= await this.contactService.readById(id)as Contact;
      if(obj){
        this.data=obj
        this.formContact.patchValue(this.data);
      }
    } catch (error) { }
  }
  async storeContacts(){
    localStorage.setItem('contacts', JSON.stringify(this.contacts));
  }
  async ngOnInit() {
    await this.loadGroups();
    this.storeGroups();
    await this.loadContacts();
    this.storeContacts();
    try {
      const id:number=parseInt(this.route.snapshot.paramMap.get('id')||"") ;
      if (!isNaN(id)) this.loadContact(id);
    } catch (error) { }
  }
  async save(){
    if (this.formContact.valid) {
      this.submitting = true;
      const value = this.formContact.value;
      Object.assign(this.data, value);
      await this.contactService.save(this.data);
      this.loadContacts();
      this.clean();
      this.submitting = false;
    } else alert('Verifique os campos antes de continuar!');
  }
  clean(){
    this.data=new Contact();
    this.formContact.reset();
  }
  editItem(id?:number){
    this.router.navigate(['/cadastro-contatos', id]);
  }
  async deleteItem(id?:number){
    if(id){
      await this.contactService.delete(id!);
      this.loadContacts();
      this.storeContacts();
    }
    this.clean();
  } 
  refreshGroups(groups: Group[]){
    this.showGroups=false;
    this.groups=groups;
    this.storeGroups();
  }
  onShowGroups(){
    this.showGroups=true;
  }
  getGroupName(id?:number){
    if(id){
      const index = this.groups.findIndex(c => c.id === id);
      if (index >= 0 && index < this.groups.length) {
        return this.groups[index]?.name;
      }
    }
    return "";
  }
  get controls() {
    return this.formContact.controls;
  }
}

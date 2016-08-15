import { Component, ViewChild, AfterViewInit } from '@angular/core';
import { CORE_DIRECTIVES } from '@angular/common';

import { ModalDirective, MODAL_DIRECTIVES, BS_VIEW_PROVIDERS } from 'ng2-bootstrap';

@Component({
    selector: 'stage-new',
    directives: [MODAL_DIRECTIVES, CORE_DIRECTIVES],
    viewProviders: [BS_VIEW_PROVIDERS],
    templateUrl: 'stage-new.component.html',
    styleUrls: ['stage-new.component.css']
})
export class StageNewComponent implements AfterViewInit {
    @ViewChild('newModal') newModal: ModalDirective;
 
    ngAfterViewInit() {}

    public showModal() {this.newModal.show(); }

    public hideModal() { this.newModal.hide(); }
}
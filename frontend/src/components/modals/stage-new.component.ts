import { Component, Output, EventEmitter, ViewChild, AfterViewInit } from '@angular/core';
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
    title: string = '';
    repo: string = '';
    branch: string = '';
    runOnClose: boolean = true;

    @ViewChild('newModal') newModal: ModalDirective;

    @Output() createNew = new EventEmitter();
 
    ngAfterViewInit() {}

    public showModal() { this.newModal.show(); }
    public hideModal() { this.newModal.hide(); }

    private onSubmit() {
        this.createNew.emit({
            value: {
                title: this.title,
                repo: this.repo,
                branch: this.branch,
                runOnClose: this.runOnClose
            }
        });
        this.hideModal();
    }
}
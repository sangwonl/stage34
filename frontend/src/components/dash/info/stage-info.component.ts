import { Component, ViewChild, AfterViewInit } from '@angular/core';
import { CORE_DIRECTIVES } from '@angular/common';

import { ModalDirective, MODAL_DIRECTIVES, BS_VIEW_PROVIDERS } from 'ng2-bootstrap';

import { Stage } from '../../../models/stage';

@Component({
    selector: 'stage-info',
    directives: [MODAL_DIRECTIVES, CORE_DIRECTIVES],
    viewProviders: [BS_VIEW_PROVIDERS],
    templateUrl: 'stage-info.component.html',
    styleUrls: ['stage-info.component.css']
})
export class StageInfoComponent implements AfterViewInit {
    @ViewChild('infoModal') infoModal: ModalDirective;
    stage: Stage;
 
    ngAfterViewInit() {}

    public showModal(stage: Stage) {
        this.stage = stage;
        this.infoModal.show();
    }

    public hideModal() { this.infoModal.hide(); }
}
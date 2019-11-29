describe('Test Set Tag', () => {
  beforeEach(() => {
    cy.visit('http://54.197.29.25:5555/projects');
  });

  it('Project exists', () => {
    cy.contains('blah').should('exist');
  });

  it('Tags exist on projects page', () => {
    cy.contains('.project-summary-container', 'blah')
      .should('contain', 'Str')
      .should('contain', 'Int')
      .should('contain', 'Float')
      .should('contain', 'None');
  });

  it('Tags exist on project page', () => {
    cy.contains('blah').click({ force: true }).then(() => {
      cy.get('.project-summary-tags-container')
        .should('contain', 'Str')
        .should('contain', 'Int')
        .should('contain', 'Float')
        .should('contain', 'None');
    });
  });

  it('Tags exist on details modal', () => {
    cy.contains('blah').click({ force: true }).then(() => {
      cy.get('.pop-up-cell').click({ force: true });
      cy.get('.container-tags')
        .should('contain', 'Str')
        .should('contain', 'Int')
        .should('contain', 'Float')
        .should('contain', 'None');
    });
  });

  it('First two tags exist in job row', () => {
    cy.contains('blah').click({ force: true }).then(() => {
      cy.get('.type-tag')
        .should('contain', 'Str')
        .should('contain', 'Int')
        .should('not.contain', 'Float')
        .should('not.contain', 'None');
    });
  });

  it('Tags exist in job row hover', () => {
    cy.contains('blah').click({ force: true }).then(() => {
      cy.contains('.type-tag', '...').trigger('mouseover', { force: true });
      cy.get('.job-cell-hover')
      .should('contain', 'Str')
      .should('contain', 'Int')
      .should('contain', 'Float')
      .should('contain', 'None');
    });
  });
});

describe('Testes de CRUD de Avisos', () => {
  beforeEach(() => {
      // Acesse a página de login e autentique
      cy.visit('http://127.0.0.1:8000');
      cy.get('input[name="username"]').type('Giulia');
      cy.get('input[name="password"]').type('Senai12345');
      cy.get('button[type="submit"]').click();

      // Certifique-se de que estamos na página inicial após o login
      cy.url().should('include', '/inicio');

      // Verifique a existência do botão de abrir modal
      cy.get('#openModalBtn').should('be.visible');
  });

  it('Deve carregar a página corretamente', () => {
      cy.contains('h1', 'Mural de Avisos').should('be.visible');
      cy.get('#openModalBtn').should('exist');
  });

  it('Deve abrir e fechar a modal de criação de aviso', () => {
      cy.get('#openModalBtn').click();
      cy.get('#modal').should('be.visible');
      cy.get('#closeModalBtn').click();
      cy.get('#modal').should('not.be.visible');
  });

  it('Deve criar um novo aviso', () => {
      cy.get('#openModalBtn').click();
      const mensagem = 'Este é um aviso de teste';
      cy.get('textarea[name="mensagem"]').type(mensagem);
      cy.get('button[type="submit"]').click();
      
      // Aguarde até que o novo aviso apareça na lista
      cy.get('.notice-list .notice-item', { timeout: 10000 }).first().should('contain', mensagem);
  });

  it('Deve editar um aviso existente', () => {
      // Primeiro, crie um aviso para garantir que há algo para editar
      const mensagemOriginal = 'Aviso original para edição';
      cy.get('#openModalBtn').click();
      cy.get('textarea[name="mensagem"]').type(mensagemOriginal);
      cy.get('button[type="submit"]').click();

      // Agora edite o aviso criado
      cy.get('.notice-item').contains(mensagemOriginal).within(() => {
          cy.get('.btn-edit').click();
      });
      
      const novaMensagem = 'Aviso editado para teste';
      cy.get('textarea[name="mensagem"]').clear().type(novaMensagem);
      cy.get('button[type="submit"]').click();
      
      // Verifique se a nova mensagem foi salva
      cy.get('.notice-item').contains(novaMensagem).should('exist');
  });

  it('Deve excluir um aviso existente', () => {
      // Primeiro, crie um aviso para garantir que há algo para excluir
      const mensagemParaExcluir = 'Aviso a ser excluído';
      cy.get('#openModalBtn').click();
      cy.get('textarea[name="mensagem"]').type(mensagemParaExcluir);
      cy.get('button[type="submit"]').click();

      // Agora exclua o aviso criado
      cy.get('.notice-item').contains(mensagemParaExcluir).within(() => {
          cy.get('.btn-delete').click();
          // Confirme a exclusão se necessário (dependendo da implementação)
          cy.on('window:confirm', () => true); // Simula a confirmação da exclusão
      });
      
      // Verifique se o aviso foi excluído
      cy.get('.notice-list').should('not.contain', mensagemParaExcluir);
  });
});
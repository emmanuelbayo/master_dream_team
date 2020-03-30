import unittest
import os

from flask import abort, url_for
from flask_testing import TestCase

from app import create_app, db
from app.models import Employee, Department, Role


class TestBase(TestCase):

    def create_app(self):

        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI = 'mysql://dt_admin:nono012369@localhost/dreamteam_test'
        )
        return app
    
    def setUp(self):

        db.create_all()

        admin = Employee(username="admin", password="admin2020",is_admin=True)

        employee = Employee(username="test-user", password="test2020")

        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):

        db.session.remove()
        db.drop_all()

class TestModel(TestBase):

    def test_employee_model(self):
        self.assertEqual(Employee.query.count(),2)

    
    def test_department_model(self):

        department = Department(name="Service informatique", 
                                description="Developpement d'application web, mobile, infographie")

        db.session.add(department)
        db.session.commit()

        self.assertEqual(Department.query.count(),1)

    def test_role_model(self):

        role = Role(name="Chef de service",description="Il est chargé du personnel du departement développement web et mobile")

        db.session.add(role)
        db.session.commit()

        self.assertEqual(Role.query.count(), 1)

class TestViews(TestBase):

    def test_homepage_view(self):

        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_view(self):

        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):

        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login',next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    
    def test_dashboard_view(self):

        target_url = url_for('home.dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,redirect_url)
    
    def test_admin_dashboard_view(self):

        target_url = url_for('home.admin_dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,redirect_url)

    def test_departments_view(self):

        target_url = url_for('admin.list_departments')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)
    
    def test_roles_view(self):

        target_url = url_for('admin.list_roles')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response, redirect_url)
    
    def test_employees_view(self):

        target_url = url_for('admin.list_employees')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

class TestErrorPages(TestBase):
    
    def test_403_forbidden(self):

        @self.app.route('/403')
        def forbidden_error():
            abort(403)
        
        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue(bytes("Erreur 403", encoding = 'utf-8') in response.data)

    def test_404_not_found(self):
        response = self.client.get('/nothinghere')
        self.assertEqual(response.status_code,404)
        self.assertTrue(bytes("Erreur 404", encoding = 'utf-8') in response.data)
    
    def test_500_internal_server_error(self):

        @self.app.route('/500')
        def internal_server_error():
            abort(500)
        
        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue(bytes("Erreur 500", encoding = 'utf-8') in response.data)


if __name__=='__main__':
    unittest.main()
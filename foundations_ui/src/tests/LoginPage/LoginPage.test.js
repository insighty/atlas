import React from 'react';
import ReactDOM from 'react-dom';
import fake from 'faker';
import LoginPage from '../../js/components/LoginPage/LoginPage';
import { shallow, mount } from 'enzyme';
import { MemoryRouter } from 'react-router-dom';
import configureTests from '../setupTests';
import ErrorMessage from '../../js/components/common/ErrorMessage';

import LoginActions from '../../js/actions/LoginActions';

configureTests();

it('Shallow Renders ProjectPage', () => {
  const wrapper = shallow(<LoginPage/>);
  expect(wrapper).toMatchSnapshot();
});

it('isLoggedIn is null by Default', () => {
    const wrapper = shallow(<LoginPage/>);
    expect(wrapper.state('isLoggedIn')).toEqual(null)
});


it("postLogin is called on Login", async () => {
    LoginActions.postLogin = jest.fn().mockResolvedValue([200, 'OK']);
    const wrapper = shallow(<LoginPage/>);
    const fake_data = {password: fake.lorem.word()};
    await wrapper.instance().login(fake_data)
    expect(LoginActions.postLogin).toBeCalledWith(fake_data)

});

it("Sets isLoggedIn to True on Login", async () => {
    LoginActions.postLogin = jest.fn().mockResolvedValue([200, 'OK']);
    const wrapper = shallow(<LoginPage/>);
    await wrapper.instance().login('data')
    expect(wrapper.state('isLoggedIn')).toEqual(true)

});

it("Sets isLoggedIn to False on Login", async () => {
    LoginActions.postLogin = jest.fn().mockResolvedValue([401, 'Unauthorized']);
    const wrapper = shallow(<LoginPage/>);
    const fake_data = {password: fake.lorem.word()};
    await wrapper.instance().login(fake_data)
    expect(wrapper.state('isLoggedIn')).toEqual(false)
});

it("Sets loginResponse on Login", async () => {
    LoginActions.postLogin = jest.fn().mockResolvedValue([200, 'OK']);
    const wrapper = shallow(<LoginPage/>);
    await wrapper.instance().login('data')
    expect(wrapper.state('loginResponse')).toEqual([200, 'OK'])
});

it("handleSubmit should call login function", async () => {
    const wrapper = shallow(<LoginPage/>);
    const wrapperInstance = wrapper.instance();
    const mockEvent = {
        preventDefault: () => '',
    }
    wrapperInstance.login = jest.fn().mockResolvedValue('cat')
    wrapperInstance.handleSubmit(mockEvent)
    expect(wrapperInstance.login).toBeCalledWith(new FormData())
});

it("handleChange should update value state", async () => {
    const wrapper = shallow(<LoginPage/>);
    const wrapperInstance = wrapper.instance();
    const mockEvent = {
        target: {value: 'dog'}
    }
    wrapperInstance.handleChange(mockEvent)
    expect(wrapper.state('value')).toEqual('dog')
});

it("calls redirect if isLoggedIn", () => {
    const wrapper = shallow(<LoginPage/>);
    LoginActions.redirect = jest.fn();
    wrapper.setState({
        isLoggedIn: true
    })
    expect(LoginActions.redirect).toBeCalledWith('/projects');
})

it("displays correct password error when unauthorized", () => {
    const wrapper = shallow(<LoginPage/>);
    wrapper.setState({
        loginResponse: [401, 'Unauthorized']
    })
    expect(wrapper.find('.auth-error').text('Incorrect password'));
})

it("displays error message when bad request", () => {  
    const wrapper = shallow(<LoginPage/>);
    wrapper.setState({
        loginResponse: [400, 'Bad Request']
    })
    expect(wrapper.find('ErrorMessage').exists()).toEqual(true);
})